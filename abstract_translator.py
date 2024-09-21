import argparse
from datetime import datetime
import requests
from bs4 import BeautifulSoup, SoupStrainer
import openai
from tqdm import tqdm

# TODO: Add ECCV, ICRA, IROS, RA-L, and other robotics and CV conferences


class ConferenceData:
    """A class to store and manage conference data."""

    def __init__(
        self, conference_name: str, year: int, total_papers: int | None = None
    ) -> None:
        self.conference_name = conference_name
        self.year = year
        self._papers = []  # List to store paper details
        self._total_papers = total_papers

    @property
    def papers(self):
        return self._papers

    @papers.setter
    def papers(self, papers):
        self._papers = papers

    def _get_conference_url(self) -> tuple:
        """Construct the URL for the conference paper page.

        Returns
        -------
        tuple
            A tuple containing the parsing URL and the base URL.
        """
        cvf_base_url = "https://openaccess.thecvf.com/"
        if self.conference_name == "CVPR":
            parsing_url = f"{cvf_base_url}CVPR{self.year}?day=all"
        elif self.conference_name == "ICCV":
            if self.year % 2 == 0:
                self.year -= 1
                print(
                    "ICCV is held every odd year. Returning the previous year's papers."
                )
            parsing_url = f"{cvf_base_url}ICCV{self.year}?day=all"
        elif self.conference_name == "ECCV":
            raise ValueError("ECCV is not implemented yet.")
        else:
            raise ValueError("Invalid conference name")
        return parsing_url, cvf_base_url

    def _fetch_papers(self) -> list:
        """Fetch the list of papers from the conference page.

        Returns
        -------
        list
            A list of dictionaries with paper titles and URLs.
        """
        parsing_url, base_url = self._get_conference_url()
        response = requests.get(parsing_url)
        soup = BeautifulSoup(
            response.content, "html.parser", parse_only=SoupStrainer("dt")
        )

        paper_list = []
        for paper in soup:
            if paper.a:
                paper_list.append({paper.a.text: {"url": base_url + paper.a["href"]}})
                if self._total_papers and len(paper_list) >= self._total_papers:
                    break
        return paper_list

    def extract_paper_abstract(self) -> list:
        """Extract abstracts for each paper.

        Returns
        -------
        list
            A list of dictionaries with paper titles, URLs, and abstracts.
        """
        self._papers = self._fetch_papers()
        for paper in tqdm(self._papers, desc="Extracting abstracts"):
            for title, info in paper.items():
                response = requests.get(info["url"])
                soup = BeautifulSoup(response.content, "html.parser")
                abstract = soup.find("div", {"id": "abstract"}).text
                info["abstract"] = abstract.strip()
        return self.papers


class Translator:
    """A class to translate the abstracts to Korean using OpenAI API"""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """A constructor to initialize the OpenAI API"""
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def translate_abstracts(self, papers: list) -> list:
        """Translate the abstracts to Korean.

        Parameters
        ----------
        papers : list
            The list of dictionaries containing paper details and abstracts

        Returns
        -------
        list
            A list of dictionaries with paper titles, URLs, abstracts, and translated abstracts
        """
        translated_papers = []
        for paper in tqdm(papers, desc="Translating abstracts"):
            for title, info in paper.items():
                abstract = info.get("abstract", "")
                prompt_system = (
                    "You are an experienced robotics and computer vision researcher "
                    "with a PhD and several years of postdoctoral experience. "
                    "Your role is to explain and translate research abstracts to junior colleagues, "
                    "specifically Korean graduate students who are new to the field."
                )
                prompt_user = (
                    f"Translate the following research abstract to Korean "
                    "in a casual way while maintaining the accuracy of the content. "
                    "For technical terms, mark the original term together in parentheses. "
                    "Do not add unnecessary greetings or additional explanations. "
                    "Simplify the language to make it easier to understand and use informal language. "
                    f"Paraphrase the content if necessary: \n\n{abstract}"
                )
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": prompt_system,
                        },
                        {
                            "role": "user",
                            "content": prompt_user,
                        },
                    ],
                    max_tokens=1024,
                    temperature=0.7,
                )
                translated_abstract = completion.choices[0].message.content
                info["translated_abstract"] = translated_abstract
                translated_papers.append({title: info})
        return translated_papers

    def save_to_file(self, translated_papers: list, filename: str) -> None:
        """Save the translated abstracts to a file.

        Parameters
        ----------
        translated_papers : list
            The list of translated papers
        filename : str
            The name of the file to save the translated abstracts
        """
        with open(filename, "a", encoding="utf-8") as file:
            for paper in tqdm(translated_papers, desc="Saving to translated papers"):
                for title, info in paper.items():
                    file.write(f"Title: {title}\n\n")
                    file.write(f"URL: {info['url']}\n\n")
                    file.write(f"Abstract: \n{info['abstract']}\n\n")
                    file.write(
                        f"Translated Abstract: \n{info['translated_abstract']}\n\n"
                    )
                    file.write("=" * 100 + "\n\n")


def initialize_parser():
    parser = argparse.ArgumentParser(description="Translate Robotics and CV papers.")
    parser.add_argument(
        "-c",
        "--conference",
        type=str,
        required=True,
        help="The name of the conference (CVPR, ICCV, ...)",
    )
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=datetime.now().year,
        help="The year of the conference (e.g., 2024)",
    )
    parser.add_argument(
        "-t",
        "--total_papers",
        type=int,
        default=None,
        help="The total number of papers to fetch. Default is all papers.",
    )
    parser.add_argument(
        "-k",
        "--api_key",
        type=str,
        required=True,
        help="The OpenAI API key",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        default=None,
        help="The name of the output file",
    )

    args = parser.parse_args()
    args.conference = args.conference.upper()
    if args.output_file is None:
        args.output_file = f"translated_{args.conference}_{args.year}.txt"

    return args


if __name__ == "__main__":
    args = initialize_parser()

    papers = ConferenceData(args.conference, args.year, args.total_papers)
    papers = papers.extract_paper_abstract()

    translator = Translator(args.api_key)
    translator.save_to_file(translator.translate_abstracts(papers), args.output_file)

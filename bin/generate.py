#! /usr/bin/env python3
"""compile exam yaml in to markdown"""
from argparse import ArgumentParser
from glob import glob
from logging import INFO, StreamHandler, getLogger
from os import makedirs, path
from re import findall
from typing import Dict, List, Tuple

from structlog import configure, dev, get_logger, processors, stdlib
from yaml import YAMLError, safe_load


class Question:
    """A exam qeustion and its answer"""

    def __init__(self, question: str, answer: str):
        self.question: str = question
        self.answer: str = answer

    def __str__(self) -> str:
        return f"1. {self.question}\n\n{self.answer}\n"


class Topic:
    """an exam topic made up multiple questions"""

    def __init__(self, title: str, questions: List[Question]):
        self.title: str = title
        self.questions: List[Question] = questions

    def __str__(self) -> str:
        questions = "\n".join(str(question) for question in self.questions)
        return f"## {self.title}\n\n{questions}"


def load_topic(topic_path: str) -> List[dict]:
    """load topic from file"""
    with open(topic_path) as file:
        try:
            return safe_load(file)
        except YAMLError:
            return []


def template_exam(exam: str, topics: List[Topic]) -> str:
    """Template out exam"""
    templated_topics = "\n".join(
        str(topic) for topic in sorted(topics, key=lambda t: t.title)
    )
    return f"# Admin Exam {exam}\n\n{templated_topics}"


def load_files(base_path: str) -> List[Tuple[str, Dict[str, List[Question]]]]:
    """load src dir"""
    logger = get_logger("load_files")
    logger.info("loading yaml files", dir=base_path)
    return [
        (topic, parse_topic(load_topic(topic))) for topic in glob(f"{base_path}/*.yaml")
    ]


def parse_topic(topic: List[dict]) -> Dict[str, List[Question]]:
    """covert a raw dictionary to a dict mapping exams to a list of questions"""
    topics_exams: Dict[str, List[Question]] = {}
    for question_dict in topic:
        question = Question(question_dict["question"], question_dict["answer"])
        for year, exams in question_dict["years"].items():
            for exam in exams:
                exam_id = f"{year}-{exam}"
                if exam_id in topics_exams:
                    topics_exams[exam_id].append(question)
                else:
                    topics_exams[exam_id] = [question]
    return topics_exams


def get_topic_name(topic_path: str) -> str:
    """convert topic file path to title"""
    title = path.splitext(path.basename(topic_path))[0]
    if not title[0].isupper():
        title = title.title()
    title_arr = findall("[A-Z][^A-Z]*", title)
    for word in title_arr:
        if len(word) == 1:
            return "".join(title_arr)
    return " ".join(title_arr)


def compile_exams(src) -> Dict[str, List[Topic]]:
    """load yaml and compile it to exam structure"""
    exams: Dict[str, List[Topic]] = {}
    for topic_path, _exams in load_files(src):
        for year, questions in _exams.items():
            topic = Topic(get_topic_name(topic_path), questions)
            if year in exams:
                exams[year].append(topic)
            else:
                exams[year] = [topic]
    return exams


def save_exam(name: str, exam: str):
    """save exam to disk"""
    logger = get_logger("save_exam")
    if path.exists(name) and (
        set(open(name).read().split("\n")) == set(exam.split("\n"))
    ):
        logger.info("skipping exam as no change", file=name)
        return
    with open(name, "w") as text_file:
        print(exam, file=text_file)
        logger.info("wrote exam to file", file=name)


def main(src: str, dest: str):
    """main function"""
    logger = get_logger("main")
    if not path.exists(dest):
        makedirs(dest)
        logger.info("created directory", dir=dest)
    for exam, topics in compile_exams(src).items():
        save_exam(f"{dest}/{exam}.md", template_exam(exam, topics))
        logger.info("exam generated", exam=exam, dest=dest)


def setup_logging():
    """setup logging"""
    configure(
        processors=[
            stdlib.add_log_level,
            processors.format_exc_info,
            stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=stdlib.LoggerFactory(),
    )

    formatter = stdlib.ProcessorFormatter(processor=dev.ConsoleRenderer())

    handler = StreamHandler()
    handler.setFormatter(formatter)

    root_logger = getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(INFO)
    return root_logger


def get_cli():
    """cli interface"""
    parser = ArgumentParser(description="compile exam metadata to exam papers")
    parser.add_argument(
        "--destination", "-d", help="directory to output exams to", default="./exams"
    )
    parser.add_argument(
        "--source", "-s", help="directory containing source material", default="./src"
    )
    return parser.parse_args()


if __name__ == "__main__":
    setup_logging()
    ARGS = get_cli()
    main(ARGS.source, ARGS.destination)

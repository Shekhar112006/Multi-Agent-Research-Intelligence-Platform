import uuid

import pytest

from app.modules.comparison.services.comparison_service import (
    ComparisonService,
)


class FakePaper:
    def __init__(
        self,
        paper_id,
        project_id,
    ):
        self.id = paper_id
        self.project_id = project_id


class FakePaperRepository:
    def __init__(self, papers):
        self.papers = papers

    def get_by_ids(self, paper_ids):
        return [
            paper
            for paper in self.papers
            if paper.id in paper_ids
        ]


def create_service(papers):
    service = ComparisonService.__new__(ComparisonService)

    service.repository = FakePaperRepository(
        papers
    )

    return service


def test_requires_at_least_two_papers():
    project_id = uuid.uuid4()
    paper_id = uuid.uuid4()

    service = create_service(
        [
            FakePaper(
                paper_id,
                project_id,
            )
        ]
    )

    with pytest.raises(
        ValueError,
        match="At least two papers",
    ):
        service.get_papers_for_comparison(
            project_id=project_id,
            paper_ids=[paper_id],
        )


def test_rejects_duplicate_papers():
    project_id = uuid.uuid4()
    paper_id = uuid.uuid4()

    service = create_service(
        [
            FakePaper(
                paper_id,
                project_id,
            )
        ]
    )

    with pytest.raises(
        ValueError,
        match="two different papers",
    ):
        service.get_papers_for_comparison(
            project_id=project_id,
            paper_ids=[
                paper_id,
                paper_id,
            ],
        )


def test_rejects_missing_paper():
    project_id = uuid.uuid4()

    paper_id_1 = uuid.uuid4()
    paper_id_2 = uuid.uuid4()

    service = create_service(
        [
            FakePaper(
                paper_id_1,
                project_id,
            )
        ]
    )

    with pytest.raises(
        ValueError,
        match="Paper\\(s\\) not found",
    ):
        service.get_papers_for_comparison(
            project_id=project_id,
            paper_ids=[
                paper_id_1,
                paper_id_2,
            ],
        )


def test_rejects_paper_from_different_project():
    project_id = uuid.uuid4()
    other_project_id = uuid.uuid4()

    paper_id_1 = uuid.uuid4()
    paper_id_2 = uuid.uuid4()

    service = create_service(
        [
            FakePaper(
                paper_id_1,
                project_id,
            ),
            FakePaper(
                paper_id_2,
                other_project_id,
            ),
        ]
    )

    with pytest.raises(
        ValueError,
        match="belong to the requested project",
    ):
        service.get_papers_for_comparison(
            project_id=project_id,
            paper_ids=[
                paper_id_1,
                paper_id_2,
            ],
        )


def test_returns_valid_papers():
    project_id = uuid.uuid4()

    paper_id_1 = uuid.uuid4()
    paper_id_2 = uuid.uuid4()

    paper_1 = FakePaper(
        paper_id_1,
        project_id,
    )

    paper_2 = FakePaper(
        paper_id_2,
        project_id,
    )

    service = create_service(
        [
            paper_1,
            paper_2,
        ]
    )

    result = service.get_papers_for_comparison(
        project_id=project_id,
        paper_ids=[
            paper_id_1,
            paper_id_2,
        ],
    )

    assert len(result) == 2
    assert result[0] is paper_1
    assert result[1] is paper_2


def test_build_comparison_data():
    from uuid import uuid4

    project_id = uuid4()
    paper_id_1 = uuid4()
    paper_id_2 = uuid4()

    class FakePaper:
        def __init__(self, paper_id, title):
            self.id = paper_id
            self.project_id = project_id
            self.title = title

    class FakePaperRepository:
        def __init__(self, db):
            pass

        def get_by_ids(self, paper_ids):
            return [
                FakePaper(paper_id_1, "Paper One"),
                FakePaper(paper_id_2, "Paper Two"),
            ]

    class FakeContent:
        def __init__(self, text):
            self.text = text

    class FakeContentRepository:
        def __init__(self, db):
            pass

        def get_by_paper_id(self, paper_id):
            if paper_id == paper_id_1:
                return FakeContent("Content of paper one.")
            return FakeContent("Content of paper two.")

    import app.modules.comparison.services.comparison_service as comparison_module

    original_paper_repository = comparison_module.PaperRepository
    original_content_repository = comparison_module.PaperContentRepository

    comparison_module.PaperRepository = FakePaperRepository
    comparison_module.PaperContentRepository = FakeContentRepository

    try:
        service = ComparisonService(db=None)

        result = service.build_comparison_data(
            project_id=project_id,
            paper_ids=[paper_id_1, paper_id_2],
        )

        assert len(result) == 2

        assert result[0]["paper_id"] == str(paper_id_1)
        assert result[0]["title"] == "Paper One"
        assert result[0]["text"] == "Content of paper one."

        assert result[1]["paper_id"] == str(paper_id_2)
        assert result[1]["title"] == "Paper Two"
        assert result[1]["text"] == "Content of paper two."

    finally:
        comparison_module.PaperRepository = original_paper_repository
        comparison_module.PaperContentRepository = original_content_repository
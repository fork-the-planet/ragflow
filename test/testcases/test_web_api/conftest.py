#
#  Copyright 2025 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import pytest
from common import (
    batch_create_datasets,
    list_kbs,
    rm_kb,
)

# from configs import HOST_ADDRESS, VERSION
from libs.auth import RAGFlowWebApiAuth
from pytest import FixtureRequest

# from ragflow_sdk import RAGFlow
from utils.file_utils import (
    create_docx_file,
    create_eml_file,
    create_excel_file,
    create_html_file,
    create_image_file,
    create_json_file,
    create_md_file,
    create_pdf_file,
    create_ppt_file,
    create_txt_file,
)


@pytest.fixture
def generate_test_files(request: FixtureRequest, tmp_path):
    file_creators = {
        "docx": (tmp_path / "ragflow_test.docx", create_docx_file),
        "excel": (tmp_path / "ragflow_test.xlsx", create_excel_file),
        "ppt": (tmp_path / "ragflow_test.pptx", create_ppt_file),
        "image": (tmp_path / "ragflow_test.png", create_image_file),
        "pdf": (tmp_path / "ragflow_test.pdf", create_pdf_file),
        "txt": (tmp_path / "ragflow_test.txt", create_txt_file),
        "md": (tmp_path / "ragflow_test.md", create_md_file),
        "json": (tmp_path / "ragflow_test.json", create_json_file),
        "eml": (tmp_path / "ragflow_test.eml", create_eml_file),
        "html": (tmp_path / "ragflow_test.html", create_html_file),
    }

    files = {}
    for file_type, (file_path, creator_func) in file_creators.items():
        if request.param in ["", file_type]:
            creator_func(file_path)
            files[file_type] = file_path
    return files


@pytest.fixture(scope="class")
def ragflow_tmp_dir(request, tmp_path_factory):
    class_name = request.cls.__name__
    return tmp_path_factory.mktemp(class_name)


@pytest.fixture(scope="session")
def WebApiAuth(auth):
    return RAGFlowWebApiAuth(auth)


# @pytest.fixture(scope="session")
# def client(token: str) -> RAGFlow:
#     return RAGFlow(api_key=token, base_url=HOST_ADDRESS, version=VERSION)


@pytest.fixture(scope="function")
def clear_datasets(request: FixtureRequest, WebApiAuth: RAGFlowWebApiAuth):
    def cleanup():
        res = list_kbs(WebApiAuth, params={"page_size": 1000})
        for kb in res["data"]["kbs"]:
            rm_kb(WebApiAuth, {"kb_id": kb["id"]})

    request.addfinalizer(cleanup)


@pytest.fixture(scope="class")
def add_dataset(request: FixtureRequest, WebApiAuth: RAGFlowWebApiAuth) -> str:
    def cleanup():
        res = list_kbs(WebApiAuth, params={"page_size": 1000})
        for kb in res["data"]["kbs"]:
            rm_kb(WebApiAuth, {"kb_id": kb["id"]})

    request.addfinalizer(cleanup)
    return batch_create_datasets(WebApiAuth, 1)[0]


@pytest.fixture(scope="function")
def add_dataset_func(request: FixtureRequest, WebApiAuth: RAGFlowWebApiAuth) -> str:
    def cleanup():
        res = list_kbs(WebApiAuth, params={"page_size": 1000})
        for kb in res["data"]["kbs"]:
            rm_kb(WebApiAuth, {"kb_id": kb["id"]})

    request.addfinalizer(cleanup)
    return batch_create_datasets(WebApiAuth, 1)[0]

from typing import AnyStr, Optional, Type, Any
from PyPDF2 import PdfReader
from gentopia.tools.basetool import *

class PdfReaderArgs(BaseModel):
    path_to_pdf: str = Field(..., description="path to the pdf file.")

class PdfTextExtractor(BaseTool):
    name = "pdf_reader"
    description = "Read text from a pdf file."
    args_schema: Optional[Type[BaseModel]] = PdfReaderArgs

    def _run(self, path_to_pdf: AnyStr) -> AnyStr:
        return self._extract_text_from_pdf(path_to_pdf)

    def _extract_text_from_pdf(self, path_to_pdf: AnyStr) -> AnyStr:
        with open(path_to_pdf, "rb") as f:
            pdf = PdfReader(f)
            text = "".join(page.extract_text() for page in pdf.pages)
        return text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    extractor = PdfTextExtractor()
    ans = extractor._run("Attention for transformer")
    print(ans)
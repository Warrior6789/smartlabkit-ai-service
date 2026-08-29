import fitz  # PyMuPDF
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.schemas.datasheet import ComponentDatasheetSummary, DatasheetParseResponse

class DatasheetService:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL_NAME,
            temperature=0,
            groq_api_key=settings.GROQ_API_KEY
        )
        self.structured_llm = self.llm.with_structured_output(ComponentDatasheetSummary)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "Bạn là một kỹ sư phần cứng IoT và hệ thống nhúng chuyên nghiệp. "
                "Nhiệm vụ của bạn là đọc nội dung trích xuất từ tài liệu datasheet kỹ thuật "
                "và bóc tách các thông số quan trọng vào đúng cấu trúc JSON được yêu cầu.\n"
                "Quy tắc:\n"
                "1. Trích xuất chính xác theo thông tin trong tài liệu.\n"
                "2. Nếu thông số nào không có trong tài liệu, hãy để chuỗi rỗng hoặc danh sách rỗng, không tự bịa đặt.\n"
                "3. Các trường danh sách (features, precautions) chỉ tóm tắt 3-5 ý quan trọng nhất."
            )),
            ("human", "Dưới đây là nội dung datasheet:\n\n{text_content}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def _clean_text(self, text: str) -> str:
        text = re.sub(r"\n\s*\n+", "\n\n", text)
        return text[:15000].strip()

    def _extract_text_from_pdf(self, pdf_bytes: bytes, max_pages: int = 4) -> tuple[str, bool]:
        doc = None
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            pages_to_read = min(len(doc), max_pages)
            extracted_pages = []
            
            for i in range(pages_to_read):
                page_text = doc[i].get_text()
                if page_text and page_text.strip():
                    extracted_pages.append(page_text.strip())
            
            if not extracted_pages:
                return "", True
            
            combined_text = "\n\n--- Page Break ---\n\n".join(extracted_pages)
            cleaned_text = self._clean_text(combined_text)
            return cleaned_text, False
        finally:
            if doc is not None:
                doc.close()

    async def parse(self, pdf_bytes: bytes) -> DatasheetParseResponse:
        try:
            raw_text, is_empty_or_scan = self._extract_text_from_pdf(pdf_bytes)
            
            if is_empty_or_scan or not raw_text:
                return DatasheetParseResponse(
                    success=False,
                    error_message="Không tìm thấy văn bản trong PDF. Tài liệu có thể là file ảnh scan hoặc bị mã hóa."
                )
            
            result: ComponentDatasheetSummary = await self.chain.ainvoke({"text_content": raw_text})
            
            return DatasheetParseResponse(
                success=True,
                data=result
            )
        except Exception as e:
            return DatasheetParseResponse(
                success=False,
                error_message=f"Lỗi trong quá trình xử lý AI: {str(e)}"
            )
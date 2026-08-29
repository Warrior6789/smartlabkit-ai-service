from pydantic import BaseModel, Field
from typing import List, Optional

class PinInfo(BaseModel):
    pin_number: str = Field(description="Tên hoặc số thứ tự chân, ví dụ: 'Pin 1' hoặc 'GPIO 21'")
    pin_name: str = Field(description="Ký hiệu chân, ví dụ: VCC, GND, TX, RX, SDA, SCL")
    description: str = Field(description="Chức năng của chân")

class ComponentDatasheetSummary(BaseModel):
    component_name: str = Field(description="Tên chính xác của linh kiện/chipset")
    category: str = Field(description="Loại linh kiện, ví dụ: Sensor, Microcontroller, Actuator, Power Module")
    operating_voltage: str = Field(description="Điện áp hoạt động, ví dụ: 3.3V - 5V DC")
    operating_current: Optional[str] = Field(None, description="Dòng điện tiêu thụ")
    communication_interfaces: List[str] = Field(description="Các chuẩn giao tiếp hỗ trợ: I2C, SPI, UART, One-Wire, PWM, ADC...")
    key_features: List[str] = Field(description="3-5 đặc tính kỹ thuật cốt lõi")
    pinout_summary: List[PinInfo] = Field(description="Danh sách các chân chính và chức năng")
    precautions: List[str] = Field(description="Các lưu ý khi cấp nguồn, nối mạch hoặc điện trở kéo (Pull-up)")

class DatasheetParseResponse(BaseModel):
    success: bool
    data: Optional[ComponentDatasheetSummary] = None
    error_message: Optional[str] = None
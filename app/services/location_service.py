from geopy.distance import geodesic
from app.models.company import Company

class LocationService:
    def is_within_range(self, user_location, company_id):
        """檢查用戶是否在允許的範圍內"""
        if not user_location:
            return False
            
        # 獲取公司資訊
        company = Company.query.get(company_id)
        if not company or not company.latitude or not company.longitude:
            return False

        company_location = (company.latitude, company.longitude)
        distance = geodesic(user_location, company_location).kilometers
        return distance <= company.clock_in_radius

    def format_location(self, latitude, longitude, address=None):
        """格式化位置信息"""
        location_str = f"({latitude}, {longitude})"
        if address:
            location_str = f"{address} {location_str}"
        return location_str 
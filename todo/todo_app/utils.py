class TodoUtils:
    @staticmethod
    def validate_time_string(time_str):
        try:
            if 'd' not in time_str or 'h' not in time_str or 'm' not in time_str:
                return False
            components = time_str.split(" ")
            days = int(components[0][:-1]) if 'd' in components[0] else 0
            hours = int(components[1][:-1]) if 'h' in components[1] else 0
            minutes = int(components[2][:-1]) if 'm' in components[2] else 0
            
            if hours>24 or minutes>60:
                return False
            
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def get_time_log_components(time_str):
        components = time_str.split(" ")
        days = int(components[0][:-1]) if 'd' in components[0] else 0
        hours = int(components[1][:-1]) if 'h' in components[1] else 0
        minutes = int(components[2][:-1]) if 'm' in components[2] else 0
        
        return [days, hours, minutes]
        
        
class JSON_exception(Exception):
    pass

class JSON_parser:
    def __init__(self,json_string):
        self.json = json_string
        self.index = 0
        self.depth = 0
        char = self._skip_whitespace()
        if char not in ["[", "{"]:
            raise JSON_exception('A JSON payload should be an object or array')


    def initializeParsing(self):
        char = self._skip_whitespace()
        if char not in ["[", "{"]:
            raise JSON_exception('A JSON payload should be an object or array')
        output = self.parse()
        try:
            char = self._skip_whitespace()
            char = self.json[self.index]
            raise JSON_exception(f"Invalid JSON: Extra character '{char}' after close.")
        except IndexError:
            pass
        return output

    def parse(self):
        char = self._skip_whitespace()

        if (char == '{'): # object start
            return self._parse_object()
        elif (char == '['):
            return self._parse_array()
        elif char in 'tfn':
            return self._parse_constant()
        elif char.isdigit() or char == '-':
            return self._parse_number()
        elif (char == '"'):
            return self._parse_string()
        else : 
            raise JSON_exception(f"Unexpected character: {char}")

    def _skip_whitespace(self):
        while (self.index < len(self.json) and self.json[self.index].isspace()):
            self.index += 1
        if (self.index < len(self.json)):
            return self.json[self.index]

        return None 
    

    def _parse_object(self):
        result = {}
        self.index += 1 # skip {
        self.depth += 1
        if (self.depth > 19):
            raise JSON_exception("Exceeds maximum depth allowed for this parser.")
        while (self.index < len(self.json)):
            char = self._skip_whitespace()

            if (char == '}'):
                self.index += 1
                self.depth -= 1
                return result
            
            if (char == ','):
                self.index += 1
            
            key = self._parse_string()
            char = self._skip_whitespace()
            if (char != ':'):
                raise JSON_exception("Expected : after key in object")

            self.index += 1 # skip :
            value = self.parse()
            result[key] = value
 
        raise JSON_exception("Expected '}'")
    
    def _parse_array(self):
        result = []
        self.index += 1
        self.depth += 1
        if (self.depth > 19):
            raise JSON_exception("Exceeds maximum depth allowed for this parser.")
        initial = True
        while (self.index < len(self.json)):
            char = self._skip_whitespace()
            if (char == ']'):
                self.index += 1
                self.depth -= 1
                return result
            if not initial:
                if (char == ','):
                    self.index += 1
                    char = self._skip_whitespace()
                    result.append(self.parse())
                else:
                    raise JSON_exception(f"Unexpected character {char}")
            else:
                initial = False
                result.append(self.parse())

        raise JSON_exception("Expected ']'")
            

    def _parse_string(self):
        result = []
        self._skip_whitespace()
        if (self.index >= len(self.json) or self.json[self.index] != '"'):
            raise JSON_exception("Expected opening '\"'")
        self.index += 1 # skip "

        while (self.index < len(self.json)):
            char = self.json[self.index]
            if (char == '"'):
                self.index += 1
                return (''.join(result))
            
            if (char == '\\'):
                self.index += 1
                if (self.index >= len(self.json)):
                    raise JSON_exception("Expected closing '\"' ")
                char = self.json[self.index]
                if (char in '''b'"ntfrbu/va\\'''):
                    result.append(f"\{char}")
                else:
                    raise JSON_exception("Illegal backslash escape sequence")
            elif (char == '\t'):
                raise JSON_exception('Invalid JSON: tab character in string')
            elif (char == '\n'):
                raise JSON_exception('Invalid JSON: line break in string')
            else:
                result.append(char)
            self.index += 1
        
        raise JSON_exception("Expected closing '\"' ")
    

    def _parse_constant(self):
        if self.json.startswith("true", self.index):
            self.index += 4
            return True
        elif self.json.startswith("false", self.index):
            self.index += 5
            return False
        elif self.json.startswith("null", self.index):
            self.index += 4
            return None
        raise JSON_exception("Invalid constant value")
    

    def _parse_number(self):
        start = self.index
        char = self.json[self.index]
        if (char == '0'):
            next_index = self.index+1
            if (next_index < len(self.json)):
                char = self.json[next_index]
                if (char in "0123456789"):
                    raise JSON_exception("Numbers cannot have leading zeroes")
                elif (char in "xXbBoO"):
                    raise JSON_exception("Only Decimal numbers are allowed")


        char = self.json[self.index]
        while ((self.index < len(self.json)) and (char in "-+0123456789.eE")):
            self.index+=1
            char = self.json[self.index]
            
        num_str = self.json[start:self.index]

        try:
            if '.' in num_str or 'e' in num_str or 'E' in num_str:
                return float(num_str)
            return int(num_str)
        except ValueError:
            raise JSON_exception(f"Invalid number : {num_str}")
        except JSON_exception:
            raise JSON_exception(f"Invalid number: {num_str}")




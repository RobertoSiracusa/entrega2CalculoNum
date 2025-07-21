
import random


def generate_scalable_bin_file_v3(file_name="", num_lines=0, max_numbers_per_line=0, number_range=(0, 65535)):
    min_val, max_val = number_range
    
    max_binary_bits = max_val.bit_length()
    max_hex_digits = (max_binary_bits + 3) // 4

    number_systems = ["decimal", "binary", "hexadecimal"]

    with open(file_name, "wb") as f:
        for _ in range(num_lines):
            generated_decimal_numbers = set() 
            current_number_count = random.randint(1, max_numbers_per_line)
            temp_line_parts = [None] * current_number_count
            idx = 0

            while len(generated_decimal_numbers) < current_number_count:

                whole_part = random.randint(min_val, max_val)
                decimal_part=float(random.randint(0,999))/1000 
                decimal_num= whole_part + decimal_part

                if decimal_num not in generated_decimal_numbers:
                    generated_decimal_numbers.add(decimal_num)

                    chosen_system = random.choice(number_systems)
                    
                    formatted_num_part = ""

                    if chosen_system == "decimal":
                        formatted_num_part = str(decimal_num)
                    elif chosen_system == "binary":
                        formatted_num_part = format(int(decimal_num), f'0{max_binary_bits}b')
                    elif chosen_system == "hexadecimal":
                        formatted_num_part = format(int(decimal_num), f'0{max_hex_digits}X')
                    
                    temp_line_parts[idx] = formatted_num_part
                    idx += 1

            line_to_write = "#".join(temp_line_parts) + "\n"
            f.write(line_to_write.encode('utf-8'))

    print(f"File '{file_name}' successfully generated with {num_lines} lines.")

if __name__ == "__main__":
    generate_scalable_bin_file_v3(
        file_name="random_representation_numbers.bin",
        num_lines=10,
        max_numbers_per_line=10,
        number_range=(-9999, 9999)
    )
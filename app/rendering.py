from html_utils import to_basic_html_page, get_html_start_block, get_html_end_block, to_heading_line, to_text_paragraph
# alla funktioner är beroende av html_utils
def format_welcome_message(visit):
    text = f"Welcome, you are visitor number {visit['id']}"
    return to_basic_html_page("Welcome", text)

#
def format_visit_history(history):
    output = get_html_start_block("Visits")
    output += to_heading_line("Visit history")
    for visit in history:
        output += to_text_paragraph(f"- {visit['timestamp']}: Visit #{visit['id']}\n")
    output += get_html_end_block()
    return output

def format_visit_details(visit):
    output = get_html_start_block("Visit details")

    output += to_heading_line(f"Visit #{visit['id']}")

    output += to_text_paragraph(f"When: {visit['timestamp']}")
    output += to_text_paragraph(f"IP: {visit['ip']}")
    output += to_text_paragraph(f"User agent: {visit['user_agent']}")

    output += get_html_end_block()
    return output

def format_hello_greeting(name):
    text = "Hello, mysterious visitor!"
    if name:
        text = f"Hello, {name}!"
    return to_basic_html_page("Hello", text)

import pandas as pd
import numpy as np
from string import Template


def main():
    # Convert list of texts (Excel file) to printable playing cards (HTML)

    excel_input = 'cards.xlsx' #'preachy.xlsx'
    html_question_output_path = '2_questions.html' # '5_preachy.html'
    html_answer_output_path = '3_answers.html' # '6_dummy.html'

    question_card_template_path = 'question_template.html'
    answer_card_template_path = 'answer_template.html'
    stylesheet_path = 'stylesheet.css'

    generate_cards(
        excel_input,
        html_question_output_path,
        html_answer_output_path,
        question_card_template_path,
        answer_card_template_path,
        stylesheet_path
    )


def generate_cards(
    excel_input_path,
    html_question_output_path,
    html_answer_output_path,
    question_card_template_path,
    answer_card_template_path,
    stylesheet_path
):
    style = '<link rel="stylesheet" href="' + stylesheet_path + '"/>'
    start = html_start(style)
    end = html_end()
    question_card_template = html_card_template(question_card_template_path)
    answer_card_template = html_card_template(answer_card_template_path)

    text_frame = pd.read_excel(excel_input_path)
    questions = text_frame['Questions'].values
    answers = text_frame['Answers'].values

    question_cards = start + generate_html_cards(questions, question_card_template) + end
    write_html_file(question_cards, html_question_output_path)

    answer_cards = start + generate_html_cards(answers, answer_card_template) + end
    write_html_file(answer_cards, html_answer_output_path)


def write_html_file(text, file_path):
    with open(file_path, "w", encoding="utf8") as output_file:
        output_file.write(text)


def generate_html_cards(questions, card_template):
    rows = 5  # 4
    columns = 4  # 3
    row_index = 1
    column_index = 1
    is_new_page = True
    is_new_row = True

    cards_html = ''
    for text in questions:
        if text is np.nan:
            continue

        if is_new_page:
            cards_html += '<table class="page">\n'
            is_new_page = False

        if is_new_row:
            cards_html += '<tr>\n'
            is_new_row = False

        cards_html += generate_card(text, card_template)

        column_index += 1
        if column_index > columns:
            cards_html += '</tr>\n'
            column_index = 1
            row_index += 1
            is_new_row = True

        if row_index > rows:
            cards_html += '</table>\n'
            row_index = 1
            is_new_page = True
    return cards_html


def generate_card(text, card_template):
    html_text = '<td>\n'
    template = Template(card_template)
    mapping = {'text': text}
    card = template.safe_substitute(mapping)
    html_text += card
    html_text += '</td>\n'
    return html_text


def html_start(style):
    start = f"""<!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8" />       
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />       
            <style>
            @media print {{
             .page {{ page-break-after: always; }}
            }}
            </style>
            {style}
        </head>
        <body>
            <div>
    """
    return start


def html_card_template(template_path):
    with open(template_path, 'r', encoding="utf8") as template_file:
        card_template = template_file.read()
        return card_template


def html_end():
    end = """
            </div>
        </body>
    </html>
    """
    return end


if __name__ == "__main__":
    main()

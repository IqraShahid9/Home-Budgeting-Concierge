from project.main_agent import run_agent
from project.memory.session_memory import SessionMemory
from project.tools.tools import parse_csv_rows
import gradio as gr

memory = SessionMemory()

def upload_csv(content):
    rows = parse_csv_rows(content)
    memory.set('uploaded_rows', rows)
    return f'Uploaded {len(rows)} rows'

def user_query(text):
    # For demo: MainAgent creates new memory; to persist across runs, write rows to file or use global memory
    # We'll write rows to a small JSON file the MainAgent could read if needed (not implemented here).
    return run_agent(text)

with gr.Blocks() as demo:
    gr.Markdown('# Home Budgeting & Bill Concierge')
    csv_in = gr.Textbox(lines=6, label='Paste CSV (header: description,amount)')
    upload_btn = gr.Button('Upload CSV')
    upload_out = gr.Textbox(label='Upload result')
    query = gr.Textbox(label='Ask the agent')
    query_btn = gr.Button('Run')
    query_out = gr.Textbox(label='Agent output')

    upload_btn.click(fn=upload_csv, inputs=[csv_in], outputs=[upload_out])
    query_btn.click(fn=lambda t: run_agent(t), inputs=[query], outputs=[query_out])

if __name__ == '__main__':
    demo.launch()


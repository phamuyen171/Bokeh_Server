from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Button, Div
from bokeh.layouts import column, row
from bokeh.driving import linear
import numpy as np
from random import uniform



# Heading H1
heading1 = Div(text="<h1>Biểu đồ Realtime - Bokeh Server</h1>", width=800)

# Heading H2
heading2 = Div(text="<h2>Cập nhật dữ liệu theo thời gian thực</h2>", width=800)

# Nội dung mô tả
description = Div(text="""
<p>Biểu đồ dưới đây hiển thị dữ liệu dạng sóng (sin + nhiễu ngẫu nhiên), cập nhật liên tục mỗi 200ms.
Bạn có thể tạm dừng hoặc tiếp tục luồng dữ liệu bằng các nút bên dưới.</p>
<p>Sử dụng <strong>Bokeh Server</strong> để xử lý cập nhật realtime phía backend.</p>
""", width=800)


# 1. Tạo nguồn dữ liệu
source = ColumnDataSource(data=dict(x=[], y=[]))

# 2. Tạo biểu đồ
p = figure(title="Realtime Stream with Bokeh",
           x_axis_label='Step',
           y_axis_label='Value',
           width=800, height=400)
p.line(x='x', y='y', source=source, line_width=2, color="navy", alpha=0.7)

# 3. Biến trạng thái và callback
callback_id = None
step_tracker = {'step': 0}  # theo dõi bước cuối cùng khi resume

# 4. Hàm cập nhật dữ liệu
@linear()
def update(step):
    s = step_tracker['step']
    new_y = np.sin(s / 10.0) + uniform(-0.1, 0.1)
    source.stream(dict(x=[s], y=[new_y]), rollover=100)
    step_tracker['step'] += 1

# 5. Nút DỪNG
stop_button = Button(label="Dừng cập nhật", button_type="danger", width=150)

def stop_callback():
    global callback_id
    if callback_id:
        curdoc().remove_periodic_callback(callback_id)
        callback_id = None
        stop_button.disabled = True
        resume_button.disabled = False
        stop_button.label = "Đã dừng"

stop_button.on_click(stop_callback)

# 6. Nút CẬP NHẬT LẠI
resume_button = Button(label="Cập nhật lại", button_type="success", width=150, disabled=True)

def resume_callback():
    global callback_id
    if callback_id is None:
        callback_id = curdoc().add_periodic_callback(update, 200)
        resume_button.disabled = True
        stop_button.disabled = False
        stop_button.label = "Dừng cập nhật"

resume_button.on_click(resume_callback)

# 7. Bắt đầu lần đầu
callback_id = curdoc().add_periodic_callback(update, 200)

# 8. Hiển thị layout
layout = column(heading1, heading2, description, p, row(stop_button, resume_button))
curdoc().add_root(layout)

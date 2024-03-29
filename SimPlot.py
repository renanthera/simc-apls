import random
import statistics as stat

from bokeh.models import BoxSelectTool, ColumnDataSource, BasicTickFormatter, HoverTool, TapTool
from bokeh.models.callbacks import CustomJS
from bokeh.models.widgets import Div
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc

box_select_callback = """
const inds = cb_obj.indices;
const d1 = ds1.data;
const d2 = ds2.data;
let temp_div2 = "pcregrep \'(.*("
for (var key in d2) {
    d2[key] = []
}
div1.text = "Total Selected: " + inds.length + "</br><table><tr><td>FR Combination</td></tr>"
for (let i = 0; i < inds.length; i++) {
    for (var key in d2) {
        d2[key].push(d1[key][inds[i]])
    }
    div1.text += "<tr>"
    div1.text += "<td>" + d1['name'][inds[i]] + "</td>"
    div1.text += "</tr>"
    temp_div2 += d1['name'][inds[i]] + "|"
}
div1.text += "</table>"
temp_div2 = temp_div2.slice(0, -1)
temp_div2 += ")[+]=tal.*)\'</br></br></br>"
div2.text = temp_div2
ds2.change.emit();
"""

TOOLTIP = """
<iframe src="https://www.raidbots.com/simbot/render/talents/@data?width=300&mini=1&level=70&bgcolor=330000" width="300" height="180"></iframe>
"""
tooltip = [('mean', '@mean'), ('name', '@name')]
hover_tool = HoverTool(tooltips=tooltip)

def rnd(u):
    try:
        return round(u)
    except:
        return u

def statistical_measures(q):
    if len(q) <= 1:
        return 'invalid dataset'
    items = {
        'mean': stat.mean(q),
        'median': stat.median(q),
        'quantiles': list(map(round, stat.quantiles(q))),
        'max': max(q),
        'min': min(q),
        'stdev': stat.stdev(q),
        'variance': stat.variance(q),
    }
    return '</br>'.join([u + ': ' + str(rnd(v)) for u,v in items.items()])

def update_stats_b(attr, old, new, ds, div):
    d = [ds.data['mean'][u] for u in new]
    text = 'selected data:</br>'
    try:
        text += statistical_measures(d)
    finally:
        div.text = text

def update_tooltip(attr, old, new, ds, div):
    d = {k: [ds.data[k][u] for u in new] for k in ds.data.keys()}
    div.text = ''
    for entry in range(len(new)):
        div.text += str({k:v[entry] for k,v in d.items()}) + '</br>'
        tal = d['data'][entry][1].split('=')[1]
        div.text += f"<iframe src=\"https://www.raidbots.com/simbot/render/talents/{tal}?width=700&level=70&bgcolor=330000\" width=\"710\" height=\"540\"></iframe></br>"

def update_data(attr, old, new, ds1, ds2, div1, div2):
    for k in ds2.data.keys():
        ds2.data[k] = []

    div1.text = "Total Selected: " + str(len(new)) + "</br><table><tr><td>FR Combination</td></tr>"
    div2.text = 'pcregrep \'(.*('

    for index in new:
        for k in ds2.data.keys():
            ds2.data[k].append(ds1.data[k][index])
        div1.text += '<tr><td>' + ds1.data['name'][index] + '</td></tr>'
        div2.text += ds1.data['name'][index] + '|'
    div1.text += '</table>'
    div2.text = div2.text[:-1] + ")[+]=tal.*)\'</br></br></br>"
    print(ds1.data)
    print(ds2.data)

def plot(data):
    ds1 = ColumnDataSource(
        data=data)
    p1 = figure(
        title='Mean DPS',
        toolbar_location='above',
        toolbar_sticky=False,
        tools='reset, wheel_zoom',
    )
    p1.add_tools(hover_tool)
    p1.add_tools(BoxSelectTool())
    p1.circle(x='random', y='mean', name='dots', source=ds1)
    p1.yaxis.formatter = BasicTickFormatter(use_scientific=False)

    ds2 = ColumnDataSource(data={k: [] for k in data.keys()})
    p2 = figure(
        title='Selection',
        tools='reset'
    )
    p2.add_tools(hover_tool)
    p2.add_tools(BoxSelectTool())
    p2.circle(x='random', y='mean', name='selection', source=ds2, size=10)
    p2.yaxis.formatter = BasicTickFormatter(use_scientific=False)

    div1 = Div()
    div2 = Div()
    div3 = Div(text='all data:</br>'+statistical_measures(data['mean']))
    div4 = Div(text='selected data:</br>')
    div5 = Div(text='')

    ds1.selected.js_on_change('indices', CustomJS(args=dict(ds1=ds1, ds2=ds2, div1=div1, div2=div2), code=box_select_callback))
    # ds1.selected.on_change('indices', lambda attr, old, new: update_data(attr, old, new, ds1, ds2, div1, div2))
    ds1.selected.on_change('indices', lambda attr, old, new: update_stats_b(attr, old, new, ds1, div4))
    ds2.selected.on_change('indices', lambda attr, old, new: update_tooltip(attr, old, new, ds1, div5))
    bottom_left = row(div3, div4)
    left = column(p1, p2, bottom_left)
    right = column(div5, div2, div1)
    layout = row(left, right)
    curdoc().add_root(layout)
    curdoc().theme = 'dark_minimal'

from flask import Flask,render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    import pandas
    import datetime
    from pandas_datareader import data
    import fix_yahoo_finance as yf
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN
    # Imports done.


    # Set up variables with the dates we will parse through.
    start_date=datetime.datetime(2016,1,1)
    end_date=datetime.datetime(2016,3,10)

    # Set up data get.
    # Date only exists for business days
    yf.pdr_override()
    df=data.get_data_yahoo(tickers="GOOG", start=start_date, end=end_date)

    pos_days=df.index[df.Close > df.Open]
    neg_days=df.index[df.Close < df.Open]

    def inc_dec(close, open):
        if close > open:
            value='Increase'
        elif close < open:
            value='Decrease'
        else:
            value='Consistent'
        return value

    df['Status']=[inc_dec(close,open) for close, open in zip(df.Close, df.Open)]
    df['Middle']=(df.Open+df.Close)/2
    df['Height']=abs(df.Open-df.Close)

    p=figure(x_axis_type='datetime', width=1000, height=300,title="CandleStick Chart for GOOG",sizing_mode='scale_width')
    p.grid.grid_line_alpha=0.3

    hours_12=12*60*60*1000

    p.segment(df.index,df.High,df.index,df.Low,color='Black')

    p.rect(df.index[df.Status=='Increase'], df.Middle[df.Status=='Increase'], width=hours_12, height=df.Height[df.Status=='Increase'],
           fill_color='#00BB11',line_color='black')

    p.rect(df.index[df.Status=='Decrease'], df.Middle[df.Status=='Decrease'], width=hours_12, height=df.Height[df.Status=='Decrease'],
           fill_color='#FF3333',line_color='black')

    script1, div1 = components(p)

    cdn_js = CDN.js_files
    cdn_css = CDN.css_files

    # Create js and css for the page that will have the bokeh plot embeded into it.
    working_js = cdn_js[0]

    working_css = cdn_css[0]

# Push the html out of the template onto the view.
    return render_template('plot.html', script1=script1, div1=div1,
    working_js=working_js, working_css=working_css)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__=='__main__':
    app.run(debug=True)

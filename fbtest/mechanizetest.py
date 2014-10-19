import mechanize
br = mechanize.Browser()
br.open("https://www.facebook.com/")
for f in br.forms():
    print f

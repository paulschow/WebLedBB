#!/usr/bin/env python

# A small python script for controlling a RGB LED
# connected to a Beaglebone Black
# over the internet

import web
from web import form
import Adafruit_BBIO.PWM as PWM

PWM.start("P9_14", 0, 2000, 1)  # red
PWM.start("P9_22", 0, 2000, 1)  # green
PWM.start("P9_16", 0, 2000, 1)  # blue



render = web.template.render('templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

# Create form
myform = form.Form(
    form.Textbox("Red",
        form.notnull,
        form.regexp('\d+', 'Must be a digit'),
        form.Validator('Must be more than 0', lambda x: int(x) >= 0),
        form.Validator('Must be less than 255', lambda x: int(x) <= 255)),
    form.Textbox("Green",
        form.notnull,
        form.regexp('\d+', 'Must be a digit'),
        form.Validator('Must be more than 0', lambda x: int(x) >= 0),
        form.Validator('Must be less than 255', lambda x: int(x) <= 255)),
    form.Textbox("Blue",
        form.notnull,
        form.regexp('\d+', 'Must be a digit'),
        form.Validator('Must be more than 0', lambda x: int(x) >= 0),
        form.Validator('Must be less than 255', lambda x: int(x) <= 255)),
    )


class index:
    def GET(self):
        return render.webledpi(myform)

    def POST(self):
        if not myform.validates():
            return render.webledpi(myform)
        else:
            #print form.d.Red
            #print form.d.Green
            #print form.d.Blue

            # Convert intputs to int
            IntRed = int(myform.d.Red)
            IntGreen = int(myform.d.Green)
            IntBlue = int(myform.d.Blue)

            print "Red = %d Blue = %d Green = %d" % (IntRed, IntGreen, IntBlue)


            #print '#%02x%02x%02x' % (IntRed, IntGreen, IntBlue)

            # Divide number by 2.55 to get value out of 100
            # And set the duty cycle of the LED
            redvalue = IntRed / 2.55
            greenvalue = IntGreen / 2.55
            bluevalue = IntBlue / 2.55
            PWM.set_duty_cycle("P9_14", redvalue)
            PWM.set_duty_cycle("P9_22", greenvalue)
            PWM.set_duty_cycle("P9_16", bluevalue)

            return render.webledpi(myform)

if __name__ == "__main__":
    web.internalerror = web.debugerror
    app.run()


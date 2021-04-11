from machine import ADC, Pin


def get_xy_analoge_inputs(x_pin, y_pin):
    x_axis = ADC(Pin(x_pin))
    y_axis = ADC(Pin(y_pin))

    # Set range of voltage
    x_axis.atten(ADC.ATTN_11DB)
    y_axis.atten(ADC.ATTN_11DB)

    return x_axis, y_axis


if __name__ == "__main__":
    x_pin = 33
    y_pin = 32

    x_axis, y_axis = get_xy_analoge_inputs(x_pin, y_pin)
    while True:
        print("X:" , x_axis.read(), "Y:", y_axis.read())

#!/usr/bin/env python
""" Generates gcode string for communicating b/w
    Aerotech printer and omnicure.
"""

__author__ = "Rodrigo Telles"
__email__ = "rtelles@g.harvard.edu"

def omni_intensity(com_port, value, cal=False):
    """ Sets the intensity of the omnicure.

    Parameters
    ----------
    com_port : int
        The com port to communicate over RS-232.
    value : float
        The intensity value to set.
    cal : bool
        Whether the omnicure is calibrated or not.
    Examples
    --------
    >>> #Set omnicure intensity on com 3 to 50%.
    >>> g.omni_intensity(com_port=3, value=50)

    """

    if cal:
        command = 'SIR{:.2f}'.format(value)
        data = calc_CRC8(command)
        gcode_var = '$strtask4="{}"'.format(data)
    else:
        command = 'SIL{:.0f}'.format(value)
        data = calc_CRC8(command)
        gcode_var = '$strtask4="{}"'.format(data)
    gcode_setInt = 'Call omniSetInt P{}'.format(com_port)

    print(f'Copy/paste following command to set omnicure intensity to {value}')
    print(f'\n\t{gcode_var}\n\t{gcode_setInt}')
    print(f'\nTo turn on omnicure use the following command\n\t`Call omniOn P{com_port}`')
    print(f'\nTo turn off omnicure use the following command\n\t`Call omniOff P{com_port}`')

def calc_CRC8(data):
    CRC8 = 0
    for letter in list(bytearray(data, encoding='utf-8')):
        for i in range(8):
            if (letter^CRC8)&0x01:
                CRC8 ^= 0x18
                CRC8 >>= 1
                CRC8 |= 0x80
            else:
                CRC8 >>= 1
            letter >>= 1
    return data +'{:02X}'.format(CRC8)

if __name__ == '__main__': 
    # import sys
    import argparse
    parser = argparse.ArgumentParser(description='Generate Aerotech gcode for setting intensity')
    parser.add_argument('-P', '--com_port', help='Omnicure COM port')
    parser.add_argument('-I', '--intensity', help='Omnicure intensity value b/w 0 and 100')
    args = parser.parse_args()
    print('\n')
    if args.com_port is None:
        print('COM port value is missing.\n\n\tExample command: `python setOmniIntensity.py --com_port=1 --intensity=50`\n')
    elif args.intensity is None:
        print('Intensity value is missing.\n\n\tExample command: `python setOmniIntensity.py --com_port=1 --intensity=50`\n')
    else:
        omni_intensity(int(args.com_port), int(args.intensity))
        # print(sys.argv)
        # assert type(int(sys.argv()))
        # omni_intensity(sys)s
    print('\n')
import seabreeze
import seabreeze.cseabreeze as csb

api = csb.SeaBreezeAPI()
api.supported_models()
print(api.supported_models())
print('---------------')

import seabreeze.pyseabreeze as psb
api = psb.SeaBreezeAPI()
print(api.supported_models())
print('---------------')

seabreeze.use('cseabreeze')
from seabreeze.spectrometers import list_devices, Spectrometer
print(list_devices())
print('---------------')
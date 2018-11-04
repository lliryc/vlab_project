import random
from models import DeviceInfo, LabInfo

if __name__ == "__main__":

    labs = LabInfo.object.all()

    for lab in labs:
        for dev_num in range(0, random.randrange(1,6)):
            rand_id =  random.choice(range(1,9778))
            device = DeviceInfo.objects.get(pk=rand_id)
            device.labinfo = lab
            device.save()

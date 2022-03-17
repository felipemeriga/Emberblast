from emberblast.conf import get_configuration
from emberblast.utils import JOBS_SECTION
from emberblast.interface import IJob


class JobMeta(type):
    def __init__(self, clsname, superclasses, attributedict):
        if clsname == 'Job':
            return
        super_class = superclasses[0]
        jobs_attributes = get_configuration('jobs').get(clsname, {})
        super_class.__init__(self, jobs_attributes.get('health_points', 0),
                             jobs_attributes.get('magic_points', 0),
                             jobs_attributes.get('move_speed', 0),
                             jobs_attributes.get('strength', 0),
                             jobs_attributes.get('intelligence', 0),
                             jobs_attributes.get('accuracy', 0),
                             jobs_attributes.get('armour', 0),
                             jobs_attributes.get('magic_resist', 0),
                             jobs_attributes.get('will', 0),
                             jobs_attributes.get('attack_type', 'melee'),
                             jobs_attributes.get('damage_vector', 'strength'),
                             )


class Job(IJob, metaclass=JobMeta):

    def __init__(self, health_points,
                 magic_points,
                 move_speed,
                 strength,
                 intelligence,
                 accuracy,
                 armour,
                 magic_resist,
                 will,
                 attack_type,
                 damage_vector):
        self.health_points = health_points
        self.magic_points = magic_points
        self.move_speed = move_speed
        self.strength = strength
        self.intelligence = intelligence
        self.accuracy = accuracy
        self.armour = armour
        self.magic_resist = magic_resist
        self.will = will
        self.attack_type = attack_type
        self.damage_vector = damage_vector

    def get_name(self):
        return self.__class__.__name__


# dynamic constructor
def constructor(self):
    pass


# dynamic example method
def display_method(self, arg):
    print(arg)


# dynamic class method
@classmethod
def class_method(cls, arg):
    print(arg)


@classmethod
def get_name(self):
    return self.name


def create_dynamic_jobs():
    jobs_dynamic_classes = {}
    job_from_config = get_configuration(JOBS_SECTION)
    for job in job_from_config:
        custom_job = type(job, (Job,), {
            # constructor
            "__init__": constructor,

            "name": job,
            # member functions
            "func_arg": display_method,
            "class_func": class_method,
            "get_name": get_name
        })
        jobs_dynamic_classes[job] = custom_job

    return jobs_dynamic_classes


dynamic_jobs_classes = create_dynamic_jobs()

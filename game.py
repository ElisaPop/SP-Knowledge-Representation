import subclasses_operations as so
import subject_operations as po
from Subclass import Subclass

entropy_list = []
entropy_zero = []
plant_list = []
subject_list = []

dk_subclass = []
dk_subject = []
to_continue = 1
seek = 0
plant = 0
subject = 0
count = 0
cnt = 0
count_subject = 0

going_to_subject = 0

max_subclass = 5
max_subject = 4


# first time it should swap directly, otherwise just remove parts of it
def swap_list(subj):
    global plant_list
    global going_to_subject

    list_to_keep = []

    if going_to_subject == 0:
        plant_list.clear()
        plant_list = subj.plant_list.copy()
        going_to_subject = 1
    else:
        for i in subj.plant_list:
            for j in plant_list:
                if i.name == j.name:
                    list_to_keep.append(j)
    plant_list = list_to_keep.copy()


if __name__ == "__main__":
    results = ()
    so.initialize()
    while to_continue:
        if seek == 0:

            if count < max_subclass:
                so.entropy_list.clear()
                so.create_entropy_list()
                entropy_list = so.entropy_list
                entropy_list.sort(key=lambda x: int(x.entropy))
                for sub in so.entropy_list:
                    for dk in dk_subclass:
                        if sub.name == dk.name:
                            if sub in entropy_list:
                                entropy_list.remove(sub)

            if plant == 1:
                if cnt == 0:
                    po.create_plant_list()
                    plant_list = po.plant_list
                    plant = 0

            if subject == 1:
                if cnt == 0:
                    po.create_subject_list()
                    subject_list = po.subject_list.copy()
                    cnt = 1
                # subject_list = po.subject_list
                # subject_list.sort(key=lambda x: int(x.frequency))
                if dk_subject.__len__() != 0:
                    copy_subj = subject_list.copy()
                    for sub1 in copy_subj:
                        for sub2 in dk_subject:
                            if sub1.name == sub2:
                                if sub1 in subject_list:
                                    subject_list.remove(sub1)
                plant = 0

        if not entropy_list and subject_list.__len__() < 1 and plant_list.__len__() < 1 and plant == 1:
            print("Plant has not been found")
            to_continue = 0
            break
        else:
            if plant == 0 and subject == 0:
                if entropy_list.__len__() < 1:
                    count_subject = 4
                else:
                    item = entropy_list[-1]
                    del entropy_list[-1]

            if plant == 1:
                if plant_list.__len__() < 1:
                    print("Plant does not match any criteria")
                    to_continue = 0
                    break
                elif subject == 0:
                    item = plant_list[1]
                    del plant_list[1]

            if subject == 1:
                if subject_list.__len__() <= 1:

                    if plant_list.__len__() < 1:
                        print("Plant does not match any criteria")
                        to_continue = 0
                        break

                        plant = 1
                        subject = 0
                        item = subject_list[1]
                        del subject_list[1]

                else:
                    if plant_list.__len__() == 1:
                        item = plant_list[0]
                        del plant_list[0]
                    else:
                        item = subject_list[1]
                        del subject_list[1]

            print("Is the plant a " + item.name + "?")
            answer = str(input())
            if answer == 'Y' or answer == 'y':
                seek = 0
                if plant == 0 and subject == 0:
                    so.append_exists(item)
                    count = count + 1

                elif plant == 1:
                    print("The plant was found.")
                    break
                elif subject == 1:
                    count_subject = count_subject + 1
                    list_to_keep = []

                    for i in item.plant_list:
                        if i in plant_list:
                            list_to_keep.append(i)
                    plant_list = list_to_keep.copy()

            elif answer == 'N' or answer == 'n':
                seek = 0
                count = count + 1
                if plant == 0 and subject == 0:
                    so.append_not_exists(item)
                elif plant == 1:
                    seek = seek + 1
                elif subject == 1:
                    count_subject = count_subject + 1
                    po.remove_plants_with_subject(item)
                    # subject_list.remove(item)

            else:
                seek = seek + 1
                if plant == 0 and subject == 0:
                    dk_subclass.append(item)
                elif subject == 1:
                    # po.append_not_exist_subject(item)
                    dk_subject.append(item.name)

            if count == max_subclass:
                subject = 1
                plant = 1
                count = count + 1

            if count_subject > max_subject:
                plant = 1
                subject = 0
                cnt = 1
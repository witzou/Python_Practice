import baker
import json
from path import path
from cytoolz import merge, join, groupby
from cytoolz.compatibility import iteritems
from cytoolz.curried import update_in
from itertools import starmap
from collections import deque
from lxml import etree, objectify
from scipy.io import savemat
from scipy.ndimage import imread


def keyjoin(leftkey, leftseq, rightkey, rightseq):
    return starmap(merge, join(leftkey, leftseq, rightkey, rightseq))


def root(folder, filename, width, height):
    E = objectify.ElementMaker(annotate=False)
    return E.annotation(
            E.folder(folder),
            E.filename(filename),
            E.source(
                E.database('MS COCO 2014'),
                E.annotation('MS COCO 2014'),
                E.image('Flickr'),
                ),
            E.size(
                E.width(width),
                E.height(height),
                E.depth(3),
                ),
            E.segmented(0)
            )


def instance_to_xml(anno):
    E = objectify.ElementMaker(annotate=False)
    xmin, ymin, width, height = anno['bbox']
    return E.object(
            E.name(anno['category_id']),
            E.bndbox(
                E.xmin(xmin),
                E.ymin(ymin),
                E.xmax(xmin+width),
                E.ymax(ymin+height),
                ),
            )


@baker.command
def write_categories(coco_annotation, dst):
    content = json.loads(path(coco_annotation).expand().text())
    categories = tuple( d['name'] for d in content['categories'])
    savemat(path(dst).expand(), {'categories': categories})


def get_instances(coco_annotation):
    coco_annotation = path(coco_annotation).expand()
    content = json.loads(coco_annotation.text())
    categories = {d['id']: d['name'] for d in content['categories']}
    return categories, tuple(keyjoin('id', content['images'], 'image_id', content['annotations']))

def rename(name, year=2014):
        out_name = path(name).stripext()
        # out_name = out_name.split('_')[-1]
        # out_name = '{}_{}'.format(year, out_name)
        return out_name


@baker.command
def create_imageset(annotations, dst):
    annotations = path(annotations).expand()
    dst = path(dst).expand()
    val_txt = dst / 'val.txt'
    train_txt = dst / 'train.txt'

    for val in annotations.listdir('*val*'):
        val_txt.write_text('{}\n'.format(val.basename().stripext()), append=True)

    for train in annotations.listdir('*train*'):
        train_txt.write_text('{}\n'.format(train.basename().stripext()), append=True)

@baker.command
def create_annotations(dbpath, subset, dst):
    annotations_path = path(dbpath).expand() / 'annotations/instances_{}2014.json'.format(subset)
    #images_path = path(dbpath).expand() / 'images/{}2014'.format(subset)
    images_path = path(dbpath).expand() / '{}2014'.format(subset)  #clw note:这里图片直接放在2014val下，前面没有images
	                                                               #         另外subset这里一般是val或者train，见文件名
    categories , instances= get_instances(annotations_path)
    dst = path(dst).expand()

    for i, instance in enumerate(instances):
        instances[i]['category_id'] = categories[instance['category_id']]

    for name, group in iteritems(groupby('file_name', instances)):
        img = imread(images_path / name)
        if img.ndim == 3:
            out_name = rename(name)
            annotation = root('VOC2014', '{}.jpg'.format(out_name), 
                              group[0]['height'], group[0]['width'])
            for instance in group:
                annotation.append(instance_to_xml(instance))
            etree.ElementTree(annotation).write(dst / '{}.xml'.format(out_name))
            #print out_name
            print(out_name) #clw modify: 看来之前是py2.7
        else:
            #print instance['file_name']
            print(instance['file_name']) #clw modify: 看来之前是py2.7





if __name__ == '__main__':
    baker.run()
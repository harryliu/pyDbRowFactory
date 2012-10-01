#! /usr/bin/env python
#coding=utf-8

import inspect
import sys

__author__ = 'Wade Liu, <wadeliu2008@gmail.com>'
__date__ = '16 Feb 2012'
__version__="0001"

##reference doc
#http://www.cnblogs.com/sevenyuan/archive/2010/12/06/1898056.html
#http://stackoverflow.com/questions/4513192/python-dynamic-class-names
#http://stackoverflow.com/questions/1796180/python-get-list-of-al-classes-within-current-module

def createInstance(full_class_name,*args,**kwargs):
    '''
    instantiate class dynamically
    [arguments]
    full_class_name: full class name that you want to instantiate, included package and module name if has
    *args: list style arguments in class constructor
    *kwargs: dict style arguments in class constructor
    [return]
    an instance of this full_class_name
    [example]
    import pyObjectCreator
    full_class_name="pck1.cls1"
    logger=pyObjectCreator.createInstance(full_class_name,'logname')
    '''
    class_meta=getClassMeta(full_class_name)
    if class_meta!=None:
        obj=class_meta(*args,**kwargs)
    else:
        obj=None
    return obj

    
def getClassMeta(full_class_name):   
    '''
    get class meta object of full_class_name, then we can use this meta object to instantiate full_class_name
    [arguments]
    full_class_name: full class name that you want to instantiate, included package and module name if has
    [return]
    an instance of this full_class_name
    [example]
    import pyObjectCreator
    full_class_name="pck1.cls1"
    loggerMeta=pyObjectCreator.getClassMeta(full_class_name)
    '''
    namespace=full_class_name.strip().rsplit('.',1)
    if len(namespace)==1:
        class_name=namespace[0]
        class_meta=_getClassMetaFromCurrModule(class_name)
    else:
        module_name=namespace[0]
        class_name=namespace[1]
        class_meta=_getClassMetaFromOtherModule(class_name,module_name)
    return class_meta
 

def _getClassMetaFromCurrModule(class_name):
    result=None
    module_name="__main__"
    for name, obj in inspect.getmembers(sys.modules[module_name]):
        if inspect.isclass(obj):
            if name==class_name:
                result=obj
                break
    return result


def _getClassMetaFromOtherModule(class_name, module_name):
    module_meta=__import__(module_name,globals(), locals(),[class_name])
    if module_meta!=None:
        class_meta=getattr(module_meta,class_name)
    else:
        class_meta=None
    return class_meta

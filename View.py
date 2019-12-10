from flask_security import current_user
from flask_admin import BaseView, expose
from flask_admin.contrib import sqla
from flask import request, abort
from Module import *


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False
        if current_user.has_role('superuser'):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
    
    can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True


class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    # form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom_index.html')


class SchoolView(BaseView):
    @expose('/', methods=['POST','GET'])
    def index(self):
        print("==================")
        if request.method == "POST":
            print(request.form.to_dict())
        _list = list()
        for i in range(1,100):
            _list.append({'row':i,'name_en':'English_en'+str(i),'name_kh':'Khmer'+str(i)})
        return self.render('admin/school_index.html', _list = _list)



class SchoolPriceView(BaseView):
    @expose('/')
    def index(self):
        _list = list()
        from Module import UserClient
        school = UserClient.query.all()
        # for x in school:
        #     _list.append({'totol_post':x.total_post})
        for i in range(1,10):
            _list.append({'row':i,'name_en':'English'+str(i),'name_kh':'Khmer'+str(i)})
        # new_list = sorted(_list, key=lambda k: k['name_en'])
        return self.render('admin/school_price.html', _list = _list)



class BacII_Post_View(BaseView):
    @expose('/', methods=['POST','GET'])
    def index(self):
        if request.method == "POST":

            print("=============================")
            print(request.form.to_dict())
            print("=============================")
            data = request.form.to_dict()
            subject_name_en = data['subject_name_en']
            subject_name_kh = data['subject_name_kh']
            obj = db.session.query(SubjectBacII).order_by(SubjectBacII.id.desc()).first()
            
            print("==================")
            print(obj.id)
            print("==================")
            # subject = SubjectBacII(id="subject1",name_en = subject_name_en, name_kh = subject_name_kh)
            # db.session.add(subject)
            # db.session.commit()
        _list = list()
        subject = list()
        for i in range(1,110):
            subject.append(i)
            _list.append({'row':i,'name_en':'English'+str(i),'name_kh':'Khmer'+str(i)})
        return self.render('admin/bacii.html', _list = _list, subject = subject)
from django.urls import path

from app_organizations.views import OrganizationCreateView, \
    OrganizationDetailView, OrganizationListView, WorkerCreateView, WorkerDetailView, WorkerListView, WorkerEditView, \
    OrganizationFileList, download_organization_file, OrganizationFileCreate, OrganizationEditView

urlpatterns = [
    path('', OrganizationListView.as_view(), name='organizations_list'),
    path('create-organization/', OrganizationCreateView.as_view(), name='organization_create'),
    path('<int:pk>', OrganizationDetailView.as_view(), name='organization_detail'),
    path('<int:pk>/edit', OrganizationEditView.as_view(), name='organization_edit'),
    path('<int:pk>/files', OrganizationFileList.as_view(), name='organization_files_list'),
    path('<int:pk>/files/create', OrganizationFileCreate.as_view(), name='organization_file_create'),
    path('files/<int:pk>/download', download_organization_file, name='organization_file_download'),
    path('workers/', WorkerListView.as_view(), name='workers_list'),
    path('workers/create-worker/', WorkerCreateView.as_view(), name='worker_create'),
    path('workers/<int:pk>', WorkerDetailView.as_view(), name='worker_detail'),
    path('workers/<int:pk>/edit', WorkerEditView.as_view(), name='worker_edit'),
]

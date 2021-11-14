from django.urls import path
from .views import Agentlist, AgentSearch, AgentSearchSort, AgentDetails


urlpatterns = [
    path('list/', Agentlist.as_view(), name='agent_list'),
    path('search/', AgentSearch.as_view(), name='agent_search'),
    #path('list/view/', AgentSearchSort.as_view(), name='agent_search_sort'),
    path('detail/<slug:slug>/', AgentDetails.as_view(), name='agent_detail'),
]

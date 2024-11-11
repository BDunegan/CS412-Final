#voter_analytics/views.py
from django.views.generic import ListView
from . models import Voter
from datetime import datetime
import plotly
import plotly.graph_objs as go
from django.views.generic import DetailView
from django.shortcuts import redirect

# Create your views here.

class VoterListView(ListView):
    '''View to display marathon results'''
    template_name = 'voter_analytics/results.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

        # Specify the fields to display
    def get_queryset(self):
        '''filters for the Voters'''
        queryset = Voter.objects.all()
        affiliation = self.request.GET.get('affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        #Order of ands for sets does not matter
        # Filter by affiliation
        if affiliation:
            queryset = queryset.filter(affiliation=affiliation)

        # Filter by date of birth range
        if min_dob:
            queryset = queryset.filter(dob__gte=f"{min_dob}-01-01")
        if max_dob:
            queryset = queryset.filter(dob__lte=f"{max_dob}-12-31")

        # Filter by voter score
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by specific election participation
        if self.request.GET.get('v20state') == 'yes':
            queryset = queryset.filter(v20state='TRUE')
        if self.request.GET.get('v21town') == 'yes':
            queryset = queryset.filter(v21town='TRUE')
        if self.request.GET.get('v21primary') == 'yes':
            queryset = queryset.filter(v21primary='TRUE')
        if self.request.GET.get('v22general') == 'yes':
            queryset = queryset.filter(v22general='TRUE')
        if self.request.GET.get('v23town') == 'yes':
            queryset = queryset.filter(v23town='TRUE')

        return queryset

    def get_context_data(self, **kwargs):
        '''pass context data to the template'''
        context = super().get_context_data(**kwargs)
        context['affiliations'] = Voter.objects.values_list('affiliation', flat=True).distinct()
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()
        context['years'] = range(1900, datetime.now().year + 1)
        return context

class VoterDetailView(DetailView):
    '''Detail view for a single Voter'''
    model = Voter
    template_name = 'voter_analytics/detail.html'
    context_object_name = 'voter'

class GraphsView(ListView):
    '''Displays three graphs which change based on filter criteria'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    #Same get_queryset as the Voters
    def get_queryset(self):
        '''filters for the graphs'''
        queryset = Voter.objects.all()
        affiliation = self.request.GET.get('affiliation')
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        voter_score = self.request.GET.get('voter_score')
        #Order of ands for sets does not matter
        # Filter by affiliation
        if affiliation:
            queryset = queryset.filter(affiliation=affiliation)

        # Filter by date of birth range
        if min_dob:
            queryset = queryset.filter(dob__gte=f"{min_dob}-01-01")
        if max_dob:
            queryset = queryset.filter(dob__lte=f"{max_dob}-12-31")

        # Filter by voter score
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by specific election participation
        if self.request.GET.get('v20state') == 'yes':
            queryset = queryset.filter(v20state='TRUE')
        if self.request.GET.get('v21town') == 'yes':
            queryset = queryset.filter(v21town='TRUE')
        if self.request.GET.get('v21primary') == 'yes':
            queryset = queryset.filter(v21primary='TRUE')
        if self.request.GET.get('v22general') == 'yes':
            queryset = queryset.filter(v22general='TRUE')
        if self.request.GET.get('v23town') == 'yes':
            queryset = queryset.filter(v23town='TRUE')

        return queryset
    
    def get_context_data(self, **kwargs):
        '''set context data for the graphs.html template'''
        # Get the default context data
        context = super().get_context_data(**kwargs)

        # Create graphs only for the filtered queryset
        voters = self.get_queryset()

        # Birth Year Distribution (Bar Chart)
        birth_years = {}
        for voter in voters:
            year = voter.dob[:4]  # First 4 characters of dob field represent the birth year
            birth_years[year] = birth_years.get(year, 0) + 1
        
        birth_year_fig = go.Figure(data=[go.Bar(
            x=list(birth_years.keys()),
            y=list(birth_years.values())
        )])
        birth_year_fig.update_layout(
            title='Distribution of Voters by Year of Birth',
            xaxis_title='Year of Birth',
            yaxis_title='Number of Voters',
            xaxis=dict(type='category')
        )
        birth_year_graph = birth_year_fig.to_html(full_html=False)
        # birth_year_graph = plotly.offline.plot(birth_year_fig, output_type='div', include_plotlyjs=False)

        # Party Affiliation Distribution (Pie Chart)
        affiliation_data = {}
        for voter in voters:
            affiliation_data[voter.affiliation] = affiliation_data.get(voter.affiliation, 0) + 1
        
        affiliation_fig = go.Figure(data=[go.Pie(
            labels=list(affiliation_data.keys()),
            values=list(affiliation_data.values())
        )])
        affiliation_fig.update_layout(
            title='Distribution of Voters by Party Affiliation'
        )
        affiliation_graph = affiliation_fig.to_html(full_html=False)
        # affiliation_graph = plotly.offline.plot(affiliation_fig, output_type='div', include_plotlyjs=False)

        # Voter Participation in Elections (Bar Chart)
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_labels = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        election_counts = [
            voters.filter(**{e: 'TRUE'}).count() for e in elections
        ]
        election_fig = go.Figure(data=[go.Bar(
            x=election_labels,
            y=election_counts
        )])
        election_fig.update_layout(
            title='Voter Participation in Elections',
            xaxis_title='Election',
            yaxis_title='Number of Voters'
        )
        election_graph = election_fig.to_html(full_html=False)
        # election_graph = plotly.offline.plot(election_fig, output_type='div', include_plotlyjs=False)

        # Add graphs and filter parameters to context
        context['birth_year_graph'] = birth_year_graph
        context['affiliation_graph'] = affiliation_graph
        context['election_graph'] = election_graph

        # Pass the available filter options to the template
        context['affiliations'] = Voter.objects.values_list('affiliation', flat=True).distinct()
        context['years'] = list(range(1900, 2024))  # Assuming birth years from 1900 to 2023
        context['voter_scores'] = Voter.objects.values_list('voter_score', flat=True).distinct()

        return context

    def form_valid(self, form):
        '''make sure the link returns to the graphs page not the Voters page'''
        # This method can be used to handle the form and redirect to the correct URL
        # Example of how to construct the redirect URL based on the filters in the GET request
        filters = self.request.GET.copy()
        return redirect(f"/va/graphs/{filters.urlencode()}")
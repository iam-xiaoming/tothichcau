import requests
from django.shortcuts import redirect, render
from django.conf import settings


CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
REDIRECT_URI = settings.REDIRECT_URI
SCOPE = 'streaming user-read-email user-read-private user-modify-playback-state user-read-playback-state'

def embed_spotify(request):
    embed_html = None
    url = request.GET.get("url")
    if url:
        try:
            oembed_url = f"https://open.spotify.com/oembed?url={url}"
            response = requests.get(oembed_url)
            if response.status_code == 200:
                embed_html = response.json().get("html")
        except Exception as e:
            print("Error:", e)
    return render(request, "spotifyplayer/embed.html", {"embed_html": embed_html})


def spotify_home(request):
    access_token = request.session.get('access_token')
    return render(request, 'spotifyplayer/spotify_home.html', {'access_token': access_token})

def spotify_login(request):
    auth_url = (
        'https://accounts.spotify.com/authorize?'
        f'client_id={CLIENT_ID}'
        f'&response_type=code'
        f'&redirect_uri={REDIRECT_URI}'
        f'&scope={SCOPE}'
    )
    print(f"Redirecting to Spotify auth: {auth_url}")  # Debug
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('spotify_home')

    token_url = 'https://accounts.spotify.com/api/token'
    try:
        response = requests.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get('access_token')
        refresh_token = token_info.get('refresh_token')
        if access_token:
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            request.session['token_expires_in'] = token_info.get('expires_in')
        else:
            print("Error: No access token in response")
            return redirect('spotify_home')
    except requests.RequestException as e:
        print(f"Error fetching access token: {e}")
        return redirect('spotify_home')

    return redirect('spotify_home')

# Add a view to refresh the token
def refresh_token(request):
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        return redirect('spotify_login')

    token_url = 'https://accounts.spotify.com/api/token'
    try:
        response = requests.post(token_url, data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        response.raise_for_status()
        token_info = response.json()
        access_token = token_info.get('access_token')
        if access_token:
            request.session['access_token'] = access_token
            request.session['token_expires_in'] = token_info.get('expires_in')
        else:
            return redirect('spotify_login')
    except requests.RequestException as e:
        print(f"Error refreshing token: {e}")
        return redirect('spotify_login')

    return redirect('spotify_home')


def spotify_refresh(request):
    refresh_token = request.session.get('refresh_token')
    if not refresh_token:
        return redirect('spotify-login')

    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=payload)
    if response.status_code == 200:
        tokens = response.json()
        request.session['access_token'] = tokens.get('access_token')
        return redirect('spotify-home')
    else:
        return redirect('spotify-login')
    
    
def spotify_search(request):
    access_token = request.session.get('access_token')
    query = request.GET.get('q', '')
    results = []
    if query and access_token:
        try:
            search_url = f'https://api.spotify.com/v1/search?q={quote(query)}&type=track,album,artist&limit=10'
            response = requests.get(search_url, headers={
                'Authorization': f'Bearer {access_token}'
            })
            response.raise_for_status()
            results = response.json()
        except requests.RequestException as e:
            print(f'Error searching Spotify: {e}')
            return render(request, 'spotifyplayer/search.html', {
                'error': 'Không thể tìm kiếm. Vui lòng thử lại.',
                'query': query
            })
    return render(request, 'spotifyplayer/search.html', {
        'results': results,
        'query': query
    })
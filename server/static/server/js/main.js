Telegram.WebApp.expand();
const tonConnectUI = new TON_CONNECT_UI.TonConnectUI({
  manifestUrl: 'https://young-paws-tap.loca.lt/static/tonconnect-manifest.json',
  buttonRootId: 'connectWallet'
});
showOffers();

document.getElementById('offersTab').addEventListener('click', function(event) {
  event.preventDefault();
  showOffers();
});

document.getElementById('leadTab').addEventListener('click', function(event) {
  event.preventDefault();
  showLeaderboard();
});

document.getElementById('friendsTab').addEventListener('click', function(event) {
  event.preventDefault();
  showFriends();
});

function showOffers() {
  document.getElementById('offersTab').classList.add('active');
  document.getElementById('leadTab').classList.remove('active');
  document.getElementById('friendsTab').classList.remove('active');
  document.getElementById('adContainer').classList.remove('hidden');
  document.getElementById('comingSoon').classList.add('hidden');
  document.getElementById('leaderboardContainer').classList.add('hidden');
  document.getElementById('currentUser').classList.add('hidden');
  document.getElementById('adContainer').scrollTo({ top: 0, behavior: 'smooth' });
}

function showLeaderboard() {
  document.getElementById('leadTab').classList.add('active');
  document.getElementById('offersTab').classList.remove('active');
  document.getElementById('friendsTab').classList.remove('active');
  document.getElementById('adContainer').classList.add('hidden');
  document.getElementById('comingSoon').classList.add('hidden');
  document.getElementById('leaderboardContainer').classList.remove('hidden');
  document.getElementById('currentUser').classList.remove('hidden');
  document.getElementById('leaderboardContainer').scrollTo({ top: 0, behavior: 'smooth' });
}

function showFriends() {
  document.getElementById('friendsTab').classList.add('active');
  document.getElementById('offersTab').classList.remove('active');
  document.getElementById('leadTab').classList.remove('active');
  document.getElementById('adContainer').classList.add('hidden');
  document.getElementById('comingSoon').classList.remove('hidden');
  document.getElementById('leaderboardContainer').classList.add('hidden');
  document.getElementById('currentUser').classList.add('hidden');
}

function sendLogToServer(message) {
  fetch(`/log_js/?message=${encodeURIComponent(message)}`)
    .then(response => response.json())
    .then(data => console.log('Log sent successfully:', data))
    .catch(error => console.error('Error sending log:', error));
}
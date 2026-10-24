"""Builds the site's pages with a shared header and footer.

Edit the page bodies below, then run: python3 build.py
"""

import hashlib

CONTACT = "support@projectAlamo.com.au"

# Changes whenever the stylesheet does, so browsers fetch the new one right
# after a deploy instead of using a cached copy.
CSS_VERSION = hashlib.sha256(open("assets/site.css", "rb").read()).hexdigest()[:10]
UPDATED = "12 October 2026"


def page(file, title, body, description):
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta property="og:site_name" content="Farenwide">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="https://www.farenwide.com/{file.removesuffix('.html').replace('index', '')}">
  <meta property="og:image" content="https://www.farenwide.com/assets/icon.png">
  <meta property="og:image:alt" content="The Farenwide app icon">
  <link rel="icon" href="assets/icon.png">
  <link rel="stylesheet" href="assets/site.css?v={CSS_VERSION}">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="index.html"><img src="assets/icon.png" alt="">Farenwide</a>
      <nav>
        <a href="videos.html">Promo videos</a>
        <a href="privacy.html">Privacy</a>
        <a href="support.html">Support</a>
      </nav>
    </div>
  </header>
  <main class="wrap">
{body}
  </main>
  <footer class="site">
    <div class="wrap">
      <a href="privacy.html">Privacy policy</a>
      <a href="terms.html">Terms of use</a>
      <a href="delete-account.html">Delete your data</a>
      <a href="support.html">Support</a>
      <a href="videos.html">Promo videos</a>
      <p>&copy; 2026 Project Alamo</p>
    </div>
  </footer>
</body>
</html>
"""
    with open(file, "w") as f:
        f.write(html)



# The design dictionary: each part of the app has one colour, used for its
# dot, label and accents everywhere on the site (tokens in assets/site.css,
# matching AppColors in the app). Listed in story order.
SECTIONS = {
    "plan": ("Plan", "Dream it up",
             "Pin places, arrange them by day, and see the route between them by foot, car "
             "or train &mdash; even drag it onto the streets you prefer."),
    "party": ("Party", "Bring your people",
              "Share a trip with friends: plan together, choose which moments to share, and "
              "see everyone&rsquo;s journey in one playback."),
    "journal": ("Journal", "Hit the road",
                "Record your path as you travel and add notes, photos, videos, voice memos and "
                "stickers right where they happened."),
    "playback": ("Playback", "Relive it",
                 "Watch your trip unfold on the map, day by day, or turn it into a vertical "
                 "story video of your photos with the map alongside, set to music from our "
                 "built-in library."),
    "assistant": ("AI assistant", "Your travel sidekick",
                  "Ask for ideas and add its picks to your map. After the trip, it finds your "
                  "best moments and turns them into a story video, with captions and hashtags "
                  "ready to share."),
    "passport": ("Passport", "Collect the stamp",
                 "Every trip earns a stamp in your travel passport, so all your adventures "
                 "live in one place."),
}

# The story of a trip: (screen, section, title, caption).
STORY_CHAPTERS = [
    ("plan", "plan", "Dream it up",
     "Pin the places you want to see, arrange them into days, and see the route between every stop."),
    ("party", "party", "Bring your people",
     "Share the trip with a simple code. Everyone sees the plan, and your journal stays private until you share it."),
    ("journal", "journal", "Hit the road",
     "Farenwide records the path you travel, and your notes and photos land right where they happened."),
    ("moments", "journal", "Keep the moments",
     "Add photos, videos, voice memos and notes as you go. That bowl of ramen deserves remembering."),
    ("playback", "playback", "Relive it",
     "Back home, watch the whole trip play back on the map, one moment at a time."),
    ("passport", "passport", "Collect the stamp",
     "Every trip earns a stamp in your travel passport, ready for the next adventure."),
]

FEATURES = """
    <section class="features">
""" + "".join(f"""      <div class="card" style="--accent:var(--{key})">
        <div class="card-banner">{name}</div>
        <div class="card-body"><h3>{title}</h3><p>{text}</p></div></div>
""" for key, (name, title, text) in SECTIONS.items()) + """    </section>
"""

STORY = """
    <section class="story" aria-labelledby="story-title">
      <div class="story-header">
        <h2 id="story-title">The story of a trip</h2>
        <p>From the first idea to the passport stamp.</p>
      </div>
      <div class="story-strip" tabindex="0" aria-label="Farenwide, chapter by chapter">
""" + "".join(f"""        <figure class="story-panel" style="--accent:var(--{section})">
          <div class="phone"><img src="assets/story/{i}-{name}.webp" width="540" height="1200"
            alt="Farenwide {SECTIONS[section][0]} screen" loading="{'eager' if i == 1 else 'lazy'}"></div>
          <figcaption>
            <span class="section-label"><span class="dot"></span>{i}. {SECTIONS[section][0]}</span>
            <h3>{title}</h3>
            <p>{text}</p>
          </figcaption>
        </figure>
""" for i, (name, section, title, text) in enumerate(STORY_CHAPTERS, 1)) + """      </div>
      <div class="story-dots">
""" + "".join(f"""        <button class="story-dot" type="button" style="--accent:var(--{section})"
          aria-label="Chapter {i}: {title}"></button>
""" for i, (_, section, title, _) in enumerate(STORY_CHAPTERS, 1)) + """      </div>
    </section>
    <script>
    // One chapter at a time: swipe, tap a dot, or let it play. It moves on by
    // itself every few seconds while in view, loops back to the start, and
    // stops for good once someone takes over (or prefers reduced motion).
    (function () {
      var strip = document.querySelector('.story-strip');
      var panels = Array.prototype.slice.call(document.querySelectorAll('.story-panel'));
      var dots = Array.prototype.slice.call(document.querySelectorAll('.story-dot'));
      if (!strip || !panels.length) return;
      var current = 0, timer = null, visible = false;
      var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      function show(i) {
        current = (i + panels.length) % panels.length;
        mark(current);
        strip.scrollTo({ left: panels[current].offsetLeft - strip.offsetLeft, behavior: still ? 'auto' : 'smooth' });
      }
      function mark(i) {
        dots.forEach(function (d, j) { d.classList.toggle('active', j === i); d.setAttribute('aria-current', j === i ? 'step' : 'false'); });
      }
      function tick() { stop(); if (visible && !still) timer = setTimeout(function () { show(current + 1); tick(); }, 4500); }
      function stop() { clearTimeout(timer); timer = null; }
      function takeOver() { still = true; stop(); }

      dots.forEach(function (d, i) { d.addEventListener('click', function () { takeOver(); show(i); }); });
      ['pointerdown', 'wheel', 'keydown', 'touchstart'].forEach(function (e) { strip.addEventListener(e, takeOver, { passive: true }); });

      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.target === strip) { visible = e.isIntersecting; tick(); }
            else if (e.isIntersecting) { current = panels.indexOf(e.target); mark(current); }
          });
        }, { root: null, threshold: 0.3 }).observe(strip);
        var inStrip = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) { if (e.isIntersecting) { current = panels.indexOf(e.target); mark(current); } });
        }, { root: strip, threshold: 0.6 });
        panels.forEach(function (p) { inStrip.observe(p); });
      }
      mark(0);
    })();
    </script>
"""

page("index.html", "Farenwide — plan, journal and relive your trips", f"""
    <section class="hero">
      <img src="assets/icon.png" alt="Farenwide app icon">
      <h1>Plan it. Live it. Relive it.</h1>
      <p class="lead">Farenwide is a travel app for planning your days, journaling as you go,
        and playing your trip back on the map &mdash; on your own or with your travel party.</p>
      <div class="get">
        <a class="badge" href="https://play.google.com/store/apps/details?id=com.projectAlamo.farenwide"
          target="_blank" rel="noopener">Get it on Google Play</a>
        <span class="soon">Coming soon to iPhone</span>
      </div>
    </section>
{STORY}
{FEATURES}""", "Farenwide: plan your days, journal as you go, and relive your trips on the map.")


page("privacy.html", "Privacy policy — Farenwide", f"""
    <article class="doc">
      <h1>Privacy policy</h1>
      <p class="updated">Last updated {UPDATED}</p>

      <p>Farenwide is built so your trips stay yours. Solo trips live only on your phone.
        Nothing is uploaded unless you share a trip with a travel party, and even then you
        choose what to share. We don&rsquo;t sell your data, show ads, or use analytics
        to track you.</p>

      <h2>What stays on your phone</h2>
      <p>Your trips, plans, journal entries, recorded paths, photos, videos and voice memos
        are stored on your device. Deleting the app deletes them.</p>

      <h2>Permissions the app asks for</h2>
      <ul>
        <li><strong>Location</strong> &mdash; to show where you are on the map and, while you
          record a trip, to draw your path (including when the screen is off). Recording only
          runs when you start it, and stops when you stop it.</li>
        <li><strong>Photos</strong> &mdash; to find photos and videos taken during a trip and
          pin them on your journal map, and to save photos you take in the app.</li>
        <li><strong>Camera and microphone</strong> &mdash; to take photos and videos and record
          voice memos for your journal.</li>
        <li><strong>Speech recognition</strong> &mdash; to turn dictation and voice memos into
          text. This uses Apple&rsquo;s speech recognition, on your device where supported.</li>
      </ul>
      <p>You can change any of these in your phone&rsquo;s Settings at any time.</p>

      <h2>Accounts (optional)</h2>
      <p>You only need an account to share trips with a travel party. You can sign in with
        Apple, Google, Facebook or an email address. We receive your name, email address and
        a sign-in identifier from the provider you choose. Accounts are managed by Google
        Firebase Authentication.</p>

      <h2>Travel parties</h2>
      <p>When you share a trip, these are stored in Google Firebase (Cloud Firestore and Cloud
        Storage, in Australia) so your party can see them:</p>
      <ul>
        <li>the trip&rsquo;s plan (places, days, routes and settings);</li>
        <li>your name and, if you set one, your avatar photo;</li>
        <li>only the journal items you choose to share, with their photos, videos or voice memos;</li>
        <li>your recorded path, if <em>Share my trail</em> is on (you can turn it off at any time,
          which removes it).</li>
      </ul>
      <p>Only members of the party can see a shared trip. You join a party with an invite code
        from someone already in it.</p>

      <h2>Services the app uses</h2>
      <ul>
        <li><strong>Mapbox</strong> provides the maps and route directions. To draw the map and
          routes, the app requests map data for the areas you view and the places you route
          between. Mapbox&rsquo;s SDK may also send anonymous usage data to Mapbox.
          See <a href="https://www.mapbox.com/legal/privacy">Mapbox&rsquo;s privacy policy</a>.</li>
        <li><strong>Apple Maps</strong> (iPhone) and <strong>Google Places</strong> (Android) look up
          the names of places you tap on the map.</li>
        <li><strong>Google Firebase</strong> handles accounts and travel parties, as described above.
          See <a href="https://firebase.google.com/support/privacy">Firebase privacy</a>.</li>
        <li><strong>Apple, Google and Facebook sign-in</strong>, if you choose them.</li>
        <li><strong>Google Gemini</strong>, run on Google Cloud, powers the optional AI features,
          which need you to be signed in. (We may instead use Anthropic&rsquo;s Claude, also run on
          Google Cloud; this page will say so.) The <em>travel assistant</em> receives your messages
          and your trip&rsquo;s title, dates and places. The <em>AI story</em> receives your
          journal&rsquo;s captions, notes and times and, only if you allow it, small previews of your
          photos and videos. These are used to answer you; under Google Cloud&rsquo;s terms they
          aren&rsquo;t used to train AI models. We keep a count of how often you use AI features,
          not what you sent.
          See <a href="https://cloud.google.com/terms/data-processing-addendum">Google Cloud&rsquo;s
          data processing terms</a>.</li>
      </ul>

      <h2>Deleting your data</h2>
      <p>You can delete your account in the app at any time, which removes everything you
        shared with travel parties. See <a href="delete-account.html">how to delete your data</a>.</p>

      <h2>Children</h2>
      <p>Farenwide isn&rsquo;t directed at children under 13, and we don&rsquo;t knowingly collect
        their personal information.</p>

      <h2>Changes</h2>
      <p>If this policy changes, we&rsquo;ll update this page and the date above.</p>

      <h2>Contact</h2>
      <p>Questions or requests: <a href="mailto:{CONTACT}">{CONTACT}</a></p>
    </article>
""", "How Farenwide handles your data.")


DELETION = f"""
    <article class="doc">
      <h1>Delete your data</h1>
      <p class="updated">Last updated {UPDATED}</p>

      <h2>Delete your account in the app</h2>
      <ol class="steps">
        <li>Open Farenwide and tap <strong>Settings</strong> (the gear icon).</li>
        <li>Tap your account (<em>Signed in as&hellip;</em>).</li>
        <li>Tap <strong>Delete account</strong> and confirm.</li>
      </ol>
      <p>This immediately deletes your account and everything you shared with travel parties:
        your profile and avatar, the journal items and media you shared, your shared trails,
        and your membership of every party. Trips on your phone stay on your phone as solo trips.</p>
      <p class="note">If you signed in a while ago, the app may ask you to sign out and back in
        first, to confirm it&rsquo;s you.</p>

      <h2>Delete some of your data, and keep your account</h2>
      <p>You can remove what you&rsquo;ve shared with a travel party without deleting your account:</p>
      <ul>
        <li><strong>A journal item and its photo, video or voice memo:</strong> open it in the
          <strong>Journal</strong> and switch off <strong>Share with travel party</strong>. It&rsquo;s
          deleted from our servers straight away and stays on your phone.</li>
        <li><strong>Your recorded trail:</strong> in the trip&rsquo;s <strong>Party</strong> tab,
          switch off <strong>Share my trail</strong>. Your uploaded trail is deleted straight away.</li>
        <li><strong>A travel party:</strong> in the trip&rsquo;s <strong>Party</strong> tab, tap
          <strong>Leave party</strong>. You&rsquo;re removed from the party and the trip stays on your
          phone as a solo trip.</li>
      </ul>
      <p>To delete anything else, such as your profile photo, email
        <a href="mailto:{CONTACT}?subject=Delete%20some%20of%20my%20Farenwide%20data">{CONTACT}</a>
        from the email address on your account and tell us what to delete. We&rsquo;ll do it within
        30 days.</p>

      <h2>Delete everything on your phone</h2>
      <p>Solo trips and your journal are stored only on your device. Deleting a trip in the app,
        or deleting the app, removes them.</p>

      <h2>Signed in with Facebook?</h2>
      <p>Deleting your account as above removes all data Farenwide holds from your Facebook
        sign-in. You can also remove Farenwide from your Facebook account under
        <em>Settings &amp; privacy &rarr; Settings &rarr; Apps and websites</em>.</p>

      <h2>Can&rsquo;t use the app?</h2>
      <p>Email <a href="mailto:{CONTACT}?subject=Delete%20my%20Farenwide%20data">{CONTACT}</a>
        from the email address on your account, and we&rsquo;ll delete your data within 30 days.</p>
    </article>
"""
for name in ("delete-account.html", "data-deletion.html"):
    page(name, "Delete your data — Farenwide", DELETION,
         "How to delete your Farenwide account and data.")


page("terms.html", "Terms of use — Farenwide", f"""
    <article class="doc">
      <h1>Terms of use</h1>
      <p class="updated">Last updated {UPDATED}</p>

      <p>By using Farenwide you agree to these terms.</p>

      <h2>Using the app</h2>
      <p>Farenwide is for planning and recording your own travels. Use it lawfully and
        respect other people&rsquo;s privacy &mdash; only share content you have the right to
        share, and don&rsquo;t use travel parties to harass or track anyone without their consent.</p>

      <h2>Your content</h2>
      <p>You own what you create. When you share items with a travel party, you let its members
        see them in the app. You can stop sharing or delete them at any time.</p>

      <h2>Maps and routes</h2>
      <p>Maps, routes, travel times and place information come from third parties and may be
        inaccurate or out of date. Always use your own judgement while travelling.</p>

      <h2>No warranty</h2>
      <p>The app is provided &ldquo;as is&rdquo;. To the extent the law allows, we&rsquo;re not
        liable for losses arising from using it. Nothing in these terms limits rights you have
        under the Australian Consumer Law.</p>

      <h2>Changes and ending</h2>
      <p>We may update these terms or the app. You can stop using the app and
        <a href="delete-account.html">delete your account</a> at any time.</p>

      <h2>Contact</h2>
      <p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
    </article>
""", "Terms of use for Farenwide.")


# Promo videos: newest first. To add one, put the MP4 (and a poster
# image) in assets/videos/ and add a line here.
VIDEOS = [
    {
        "file": "journal-recording",
        "section": "journal",
        "title": "Record your path as you travel",
        "text": "Tap Start recording and Farenwide draws your route on the map as you walk. "
                "Here, an evening stroll through Gion in Kyoto: it keeps recording with the app "
                "in the background, with a notification so you always know it's on, and it "
                "stays on your phone.",
        "length": "1:51",
    },
]

page("videos.html", "Promo videos — Farenwide", """
    <article class="videos">
      <h1>Promo videos</h1>
      <p class="lead">See Farenwide in action. Feel free to share these.</p>
""" + "".join(f"""      <figure class="video-card" style="--accent:var(--{v['section']})">
        <video controls playsinline preload="metadata" poster="assets/videos/{v['file']}.jpg"
          width="540" height="1200">
          <source src="assets/videos/{v['file']}.mp4" type="video/mp4">
        </video>
        <figcaption>
          <span class="section-label"><span class="dot"></span>{SECTIONS[v['section']][0]} · {v['length']}</span>
          <h2>{v['title']}</h2>
          <p>{v['text']}</p>
          <a href="assets/videos/{v['file']}.mp4" download>Download video</a>
        </figcaption>
      </figure>
""" for v in VIDEOS) + """    </article>
""", "Short videos of Farenwide in action: plan, journal and relive your trips.")


page("support.html", "Support — Farenwide", f"""
    <article class="doc">
      <h1>Support</h1>
      <p>Questions, ideas or something not working? Email
        <a href="mailto:{CONTACT}">{CONTACT}</a> and we&rsquo;ll get back to you.</p>

      <h2>Common questions</h2>
      <p><strong>Do I need an account?</strong> No. Solo trips work without one and stay on your
        phone. You only need an account to share a trip with a travel party.</p>
      <p><strong>How do I join a friend&rsquo;s trip?</strong> Ask them for an invite code (Party tab
        &rarr; Invite), then tap <em>Join a party</em> on your trips list and enter it.</p>
      <p><strong>Who can see my journal?</strong> Only you, unless you open an item and switch on
        <em>Share with travel party</em>.</p>
      <p><strong>How do I delete my data?</strong> See <a href="delete-account.html">Delete your data</a>.</p>
    </article>
""", "Get help with Farenwide.")

print("built")

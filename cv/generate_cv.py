#!/usr/bin/env python3
"""
Generates kasun-hapangama.pdf (the site's resume, linked from index.html's
"Resume (PDF)" buttons) from the content in this file.

Plain, standard ATS-format CV: Arial, black on white, single column, no
colored/decorative layout elements aside from the header photo, the two
certification badge images (read directly from assets/web/ so they stay in
sync with what the site itself uses), and a small QR code linking to
kasun.hapangama.com (cv/qr-site.png, pre-generated, regenerate it with the
qrcode package if the URL ever changes).

Usage:
    python3 cv/generate_cv.py

Requires:
    - Google Chrome (or Chromium) installed locally, for headless print-to-pdf.
    - No other dependencies (stdlib only).

To update the CV: edit the CONTENT section below, then rerun this script.
It always writes to <repo root>/kasun-hapangama.pdf.
"""
import base64
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PDF = ROOT / "kasun-hapangama.pdf"

AVATAR = ROOT / "cv/avatar-headshot.jpg"  # cropped/zoomed from assets/web/avatar.jpg for a clearer face at small print size
AWS_BADGE = ROOT / "assets/web/badges/aws-saa.png"
OCA_BADGE = ROOT / "assets/web/badges/oca-java.png"
QR_CODE = ROOT / "cv/qr-site.png"  # pre-generated, points to https://kasun.hapangama.com/


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def find_chrome() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
    ]
    for c in candidates:
        if Path(c).exists():
            return c
        found = shutil.which(c)
        if found:
            return found
    sys.exit(
        "Could not find Google Chrome or Chromium on this machine.\n"
        "Install Chrome, or edit find_chrome() in cv/generate_cv.py to point "
        "at your browser binary."
    )


# ===========================================================================
# CONTENT - edit this to update the CV, then rerun the script.
# Every date, bullet, link, and number below should match what's live on
# kasun.hapangama.com (index.html) - keep them in sync when either changes.
# Never use em dashes (-) anywhere in this content; use a comma or "to".
# ===========================================================================

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Kasun Hapangama - Resume</title>
<style>
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
@page{ size:A4; margin:14mm 18mm; }
body{
  font-family:Arial, Helvetica, sans-serif; color:#000; background:#fff;
  font-size:10pt; line-height:1.3;
}
a{ color:#000; text-decoration:none; }

h1,h2,h3,p,ul,li{ margin:0; padding:0; }

.header{ display:flex; align-items:center; gap:5mm; break-inside:avoid; page-break-inside:avoid; }
.photo{ width:22mm; height:22mm; border-radius:50%; object-fit:cover; flex:0 0 auto; }
.header-mid{ flex:1 1 auto; text-align:center; }
.name{ font-size:19pt; font-weight:bold; letter-spacing:.02em; }
.role{ font-size:10.6pt; margin-top:.6mm; }
.contact{ font-size:9pt; margin-top:1.6mm; }
.contact span{ margin:0 1mm; }
.badges{ display:flex; flex-direction:row; gap:2.4mm; flex:0 0 auto; align-items:center; }
.badges img{ width:18mm; height:18mm; object-fit:contain; }

.section--overlay{ position:relative; }
.qr-overlay{ position:absolute; top:6.5mm; right:0; }
.qr-overlay img{ width:15mm; height:15mm; object-fit:contain; display:block; }

.section{ margin-top:4mm; }
.section h2{
  font-size:10.6pt; font-weight:bold; text-transform:uppercase; letter-spacing:.03em;
  border-bottom:1px solid #000; padding-bottom:.8mm; margin-bottom:2mm;
  break-after:avoid; page-break-after:avoid;
}

.summary{ text-align:justify; }

.entry{ margin-bottom:2.6mm; break-inside:avoid; page-break-inside:avoid; }
.entry:last-child{ margin-bottom:0; }
.entry-top{ display:flex; justify-content:space-between; align-items:baseline; gap:4mm; }
.entry-title{ font-weight:bold; font-size:10.2pt; }
.entry-sub{ font-style:italic; font-size:9.6pt; }
.entry-link{ font-size:8.8pt; }
.entry-date{ font-size:9.2pt; white-space:nowrap; text-align:right; }
ul.bullets{ margin:1mm 0 0; padding-left:4.6mm; }
ul.bullets li{ margin:.4mm 0; }

.skills-row{ margin:.6mm 0; font-size:9.6pt; break-inside:avoid; page-break-inside:avoid; }
.skills-row b{ font-weight:bold; }

.two{ display:flex; justify-content:space-between; gap:4mm; margin:.5mm 0; break-inside:avoid; page-break-inside:avoid; }
.two .l{ font-weight:bold; font-size:9.8pt; }
.two .r{ font-size:9.2pt; }

.cert-line, .award-line{ margin:.5mm 0; font-size:9.6pt; break-inside:avoid; page-break-inside:avoid; }
</style>
</head>
<body>
<div class="page">

  <div class="header">
    <img class="photo" src="data:image/jpeg;base64,__AVATAR__" alt="">
    <div class="header-mid">
      <div class="name">KASUN HAPANGAMA</div>
      <div class="role">Software Engineer</div>
      <div class="contact">
        <span>Malabe, Sri Lanka</span>&bull;
        <span><a href="tel:+94766370705">+94 76 637 0705</a></span>&bull;
        <span><a href="mailto:kasun@hapangama.com">kasun@hapangama.com</a></span>&bull;
        <span><a href="https://kasun.hapangama.com/">kasun.hapangama.com</a></span>&bull;
        <span><a href="https://www.linkedin.com/in/kaxun/">linkedin.com/in/kaxun</a></span>&bull;
        <span><a href="https://github.com/ka0un/">github.com/ka0un</a></span>
      </div>
    </div>
    <div class="badges">
      <img src="data:image/png;base64,__AWS_BADGE__" alt="AWS Certified Solutions Architect - Associate">
      <img src="data:image/png;base64,__OCA_BADGE__" alt="Oracle Certified Associate, Java SE 8">
    </div>
  </div>

  <div class="section">
    <h2>Summary</h2>
    <p class="summary">Software engineer with 3+ years building secure REST APIs and enterprise web applications in Java and .NET for clients across Japan, contracting through SoftSora. Founder of SUNDEVS, leading the engineering team that builds and sells commercial developer tools with 1,000+ copies sold. AWS Certified Solutions Architect, Associate, and Oracle Certified Associate in Java SE 8. Work spans car marketplace platforms, generative-AI sales tooling, and open source security software, with 30+ projects completed. Currently studying Software Engineering at SLIIT.</p>
  </div>

  <div class="section">
    <h2>Skills</h2>
    <p class="skills-row"><b>Languages:</b> Java, C#, JavaScript, TypeScript</p>
    <p class="skills-row"><b>Backend &amp; Frameworks:</b> Spring Boot, ASP.NET, NestJS, Hibernate, Thymeleaf</p>
    <p class="skills-row"><b>Databases:</b> MySQL, MongoDB, Redis, Oracle DB</p>
    <p class="skills-row"><b>Cloud &amp; DevOps:</b> AWS, Oracle Cloud, Docker, Kubernetes, Kafka, Nginx</p>
    <p class="skills-row"><b>AI &amp; Automation:</b> Claude AI, Gemini, n8n, Selenium</p>
    <p class="skills-row"><b>Tools &amp; Platforms:</b> Git, GitHub, HubSpot, Zoho CRM</p>
  </div>

  <div class="section">
    <h2>Experience</h2>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">SoftSora, Software Engineer</div>
        <div class="entry-date">Dec 2025 to Present</div>
      </div>
      <div class="entry-sub">Nugegoda, Sri Lanka</div>
      <ul class="bullets">
        <li>Architect and own core systems, from technical design through production delivery.</li>
        <li>Full stack development across React, Next.js, Node.js, Nest.js, Express.js, Spring Boot and .NET.</li>
        <li>Work within an Agile/Scrum process, including sprint planning and regular standups.</li>
        <li>Own software testing, project management, documentation, and stakeholder collaboration.</li>
        <li>Run DevOps on AWS and Oracle Cloud, from CI/CD to deployment and monitoring.</li>
        <li>Drive automation using Claude AI, Gemini, and n8n for internal tooling and client sales workflows.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">SoftSora, Junior Software Engineer</div>
        <div class="entry-date">Dec 2024 to Dec 2025</div>
      </div>
      <div class="entry-sub">Colombo, Sri Lanka</div>
      <ul class="bullets">
        <li>Designed and built features for a car marketplace client project using Spring Framework and .NET.</li>
        <li>Collaborated directly with the client on requirements gathering, documentation, and delivery.</li>
        <li>Managed software project timelines and customer collaboration.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">SoftSora, Software Engineer Intern</div>
        <div class="entry-date">Jun 2024 to Dec 2024</div>
      </div>
      <div class="entry-sub">Colombo, Sri Lanka</div>
      <ul class="bullets">
        <li>Built REST APIs with authentication and access control for merchant registration on the car marketplace project.</li>
        <li>Enabled system access for 1,000+ merchants.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">SUNDEVS, Founder and Developer <span class="entry-link">(side venture, alongside full-time SoftSora role)</span></div>
        <div class="entry-date">Apr 2023 to Present</div>
      </div>
      <div class="entry-sub">Sri Lanka <span class="entry-link">(store.sundevs.net)</span></div>
      <ul class="bullets">
        <li>Founded and run SUNDEVS, building and selling commercial developer tools.</li>
        <li>Lead a software engineering team to build our products.</li>
        <li>1,000+ copies sold across commercial developer tools.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">Summit Realms, Plugin Developer</div>
        <div class="entry-date">Oct 2023 to Feb 2024</div>
      </div>
      <div class="entry-sub">Remote</div>
      <ul class="bullets">
        <li>Built custom server side addons and an event management system for Spigot servers.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>Selected Projects</h2>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">Car Marketplace Buyer Registration Platform</div>
        <div class="entry-date">2024</div>
      </div>
      <div class="entry-sub">SoftSora, Client: a Japanese car marketplace, Osaka, Japan</div>
      <ul class="bullets">
        <li>Built a self service web platform (Java, Spring Boot, React, AWS EC2, RDS/PostgreSQL, CloudFront) replacing manual Excel and email for buyer registration.</li>
        <li>Car matching preferences, a personal dashboard, and automated match notifications via AWS SNS/SES.</li>
        <li>1,000+ buyers registered and onboarded on the platform.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">Car Marketplace Vehicle Data Platform</div>
        <div class="entry-date">2024</div>
      </div>
      <div class="entry-sub">SoftSora, Client: a Japanese car marketplace</div>
      <ul class="bullets">
        <li>Re-architected a static vehicle data set into a dynamic model on AWS S3 and CloudFront with an EC2 microservice.</li>
        <li>Cut data publishing time from 1 to 2 days down to a few hours, with sub 1ms reads after initial load.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">OPProtector (Open Source) <span class="entry-link">(github.com/ka0un/OPProtector)</span></div>
        <div class="entry-date">2023 to Present</div>
      </div>
      <ul class="bullets">
        <li>Real time security plugin monitoring Minecraft operator accounts for compromise and unauthorized access.</li>
        <li>19,000+ servers protected and counting; 75+ GitHub stars; zero false positives via intelligent detection.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">AI Powered Sales Proposal Engine</div>
        <div class="entry-date">2026</div>
      </div>
      <div class="entry-sub">SoftSora, Client: a marketing agency, Japan</div>
      <ul class="bullets">
        <li>Built an engine that reads client records plus dozens of public signals to generate context aware, market tuned sales proposals.</li>
        <li>Reduced hour long manual prospect research to seconds, with consistent proposal quality.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-top">
        <div class="entry-title">CRM Unification and AI Enrichment</div>
        <div class="entry-date">2026</div>
      </div>
      <div class="entry-sub">SoftSora, Client: a B2B marketing agency, Japan</div>
      <ul class="bullets">
        <li>Merged three disconnected contact sources into one CRM and normalized 79 job title variations.</li>
        <li>3,000+ genuine decision makers identified from about 6,700 contacts; about 6,000 records enriched at scale.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>Commercial Products, SUNDEVS</h2>
    <div class="two"><div class="l">SunLicense, license key management with a Java API, Discord bot, and docs</div><div class="r"><a href="https://store.sundevs.net/l/sunlicense">store.sundevs.net/l/sunlicense</a></div></div>
    <div class="two"><div class="l">SunGuard, wraps ProGuard and yGuard to obfuscate Java code</div><div class="r"><a href="https://store.sundevs.net/l/sunguard">store.sundevs.net/l/sunguard</a></div></div>
    <div class="two"><div class="l">SunPaste, self hosted paste sharing with a REST API and admin panel</div><div class="r"><a href="https://store.sundevs.net/l/sunpaste">store.sundevs.net/l/sunpaste</a></div></div>
    <div class="two"><div class="l">SunLinks, self hostable URL shortener with click tracking and analytics</div><div class="r"><a href="https://store.sundevs.net/l/sunlinks">store.sundevs.net/l/sunlinks</a></div></div>
  </div>

  <div class="section">
    <h2>Education</h2>
    <div class="two"><div class="l">SLIIT, BSc (Hons) Information Technology, Software Engineering</div><div class="r">Aug 2023 to Jul 2027</div></div>
    <div class="two"><div class="l">SLIIT, Higher Diploma in Information Technology</div><div class="r">Aug 2023 to Jul 2025</div></div>
    <div class="two"><div class="l">Nalanda College, Colombo</div><div class="r">2020 to 2023</div></div>
    <div class="two"><div class="l">Carey College, Colombo 08</div><div class="r">2009 to 2020</div></div>
  </div>

  <div class="section">
    <h2>Certifications</h2>
    <p class="cert-line">AWS Certified Solutions Architect, Associate, Amazon Web Services <a href="https://www.credly.com/badges/52a14006-7ffb-48a5-809f-7b1874bfa108">(verify)</a></p>
    <p class="cert-line">Oracle Certified Associate, Java SE 8, Oracle <a href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=DB2B9B81F39ADD3B975B1DC33C8CC3F5B9597B75F563EC1816539DB3AD980EB2">(verify)</a></p>
    <p class="cert-line">OCI Certified Foundations Associate, Oracle <a href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=9A0A1BF53722B80017C3B92E76871C82F0534FD07613DC90C6A82A8E052DBE3A">(verify)</a></p>
    <p class="cert-line">OCI Certified AI Foundations Associate, Oracle <a href="https://catalog-education.oracle.com/ords/certview/sharebadge?id=05A77EA2079F47E065129ABDE670150E05BEA3106D3AC38E2FC2C28F5E531B41">(verify)</a></p>
  </div>

  <div class="section section--overlay">
    <h2>Awards</h2>
    <p class="award-line">SLIIT Dean's List Award, Year 1 Semester 2</p>
    <p class="award-line">SLIIT Dean's List Award, Year 2 Semester 2</p>
    <a class="qr-overlay" href="https://kasun.hapangama.com/">
      <img src="data:image/png;base64,__QR_CODE__" alt="QR code linking to kasun.hapangama.com">
    </a>
  </div>

</div>
</body>
</html>
"""


def build() -> None:
    html = (
        TEMPLATE.replace("__AVATAR__", b64(AVATAR))
        .replace("__AWS_BADGE__", b64(AWS_BADGE))
        .replace("__OCA_BADGE__", b64(OCA_BADGE))
        .replace("__QR_CODE__", b64(QR_CODE))
    )

    if "—" in html or "&mdash;" in html:
        sys.exit("Refusing to build: found an em dash in the CV content. Remove it and rerun.")

    chrome = find_chrome()

    with tempfile.TemporaryDirectory() as tmp:
        html_path = Path(tmp) / "resume.html"
        html_path.write_text(html, encoding="utf-8")

        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={OUTPUT_PDF}",
                html_path.as_uri(),
            ],
            check=True,
            capture_output=True,
        )

    print(f"Wrote {OUTPUT_PDF}")


if __name__ == "__main__":
    build()

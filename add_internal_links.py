#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Define the blog directory
BLOG_DIR = "/sessions/funny-vibrant-thompson/mnt/Loot/affiliate-site/output/blog"

# Mapping of blog posts to their internal links
LINK_CLUSTERS = {
    "at-home-microneedling-safe": {
        "cta_links": [
            {"url": "/microneedling-devices/", "label": "Microneedling Devices Reviews →"},
            {"url": "/blog/dermaroller-vs-microneedling-pen/", "label": "Dermaroller vs Microneedling Pen →"}
        ],
        "related_articles": [
            {"url": "/blog/dermaroller-vs-microneedling-pen/", "label": "Dermaroller vs Microneedling Pen: Which Works Better?"}
        ]
    },
    "best-ipl-devices-dark-skin": {
        "cta_links": [
            {"url": "/at-home-laser-hair-removal/", "label": "At-Home Laser Hair Removal →"},
            {"url": "/blog/ipl-vs-laser-hair-removal-home/", "label": "IPL vs Laser Hair Removal →"}
        ],
        "related_articles": [
            {"url": "/blog/how-many-ipl-sessions/", "label": "How Many IPL Sessions Do You Actually Need?"},
            {"url": "/blog/ipl-vs-laser-hair-removal-home/", "label": "IPL vs Laser Hair Removal: Which Is Better?"}
        ]
    },
    "best-teeth-whitening-sensitive": {
        "cta_links": [
            {"url": "/teeth-whitening/", "label": "Teeth Whitening Reviews →"},
            {"url": "/blog/snow-vs-hismile-teeth-whitening/", "label": "Snow vs HiSmile Whitening →"}
        ],
        "related_articles": [
            {"url": "/blog/snow-vs-crest-whitestrips/", "label": "Snow vs Crest Whitestrips: Which Works Faster?"}
        ]
    },
    "curology-vs-hers-skincare": {
        "cta_links": [
            {"url": "/prescription-skincare/", "label": "Prescription Skincare Reviews →"},
            {"url": "/blog/tretinoin-vs-retinol-difference/", "label": "Tretinoin vs Retinol →"}
        ],
        "related_articles": [
            {"url": "/blog/hims-vs-hers-comparison/", "label": "Hims vs Hers: Which Telehealth Service Is Best?"}
        ]
    },
    "find-good-med-spa": {
        "cta_links": [
            {"url": "https://clinovyr.com", "label": "Clinovyr Med Spa Directory →"},
            {"url": "/blog/nuface-microcurrent-review/", "label": "NuFace Microcurrent Review →"}
        ],
        "related_articles": [
            {"url": "/blog/dermaroller-vs-microneedling-pen/", "label": "Dermaroller vs Microneedling Pen"},
            {"url": "/blog/led-light-therapy-masks-work/", "label": "Do LED Light Therapy Masks Actually Work?"}
        ]
    },
    "hims-vs-hers-comparison": {
        "cta_links": [
            {"url": "/hair-loss-treatments/", "label": "Hair Loss Treatments →"},
            {"url": "/blog/minoxidil-for-women-hair-loss/", "label": "Minoxidil for Women's Hair Loss →"}
        ],
        "related_articles": [
            {"url": "/blog/hims-vs-keeps-hair-loss/", "label": "Hims vs Keeps: Which Hair Loss Treatment Works?"},
            {"url": "/blog/curology-vs-hers-skincare/", "label": "Curology vs Hers Skincare Comparison"}
        ]
    },
    "hims-vs-keeps-hair-loss": {
        "cta_links": [
            {"url": "/hair-loss-treatments/", "label": "Hair Loss Treatments →"},
            {"url": "/blog/minoxidil-for-women-hair-loss/", "label": "Minoxidil for Women's Hair Loss →"}
        ],
        "related_articles": [
            {"url": "/blog/hims-vs-hers-comparison/", "label": "Hims vs Hers: A Complete Comparison"},
            {"url": "/blog/best-ipl-devices-dark-skin/", "label": "Best IPL Devices for Dark Skin"}
        ]
    },
    "how-many-ipl-sessions": {
        "cta_links": [
            {"url": "/at-home-laser-hair-removal/", "label": "At-Home Laser Hair Removal →"},
            {"url": "/blog/ipl-vs-laser-hair-removal-home/", "label": "IPL vs Laser Hair Removal →"}
        ],
        "related_articles": [
            {"url": "/blog/best-ipl-devices-dark-skin/", "label": "Best IPL Devices for Dark Skin Tones"},
            {"url": "/blog/ipl-vs-laser-hair-removal-home/", "label": "IPL vs Laser: Which Is Better?"}
        ]
    },
    "led-light-therapy-masks-work": {
        "cta_links": [
            {"url": "/led-light-therapy-masks/", "label": "LED Light Therapy Masks →"},
            {"url": "/blog/red-light-therapy-face-benefits/", "label": "Red Light Therapy Benefits →"}
        ],
        "related_articles": [
            {"url": "/blog/red-light-therapy-face-benefits/", "label": "Red Light Therapy for Face: Benefits & Science"},
            {"url": "/blog/best-led-mask-for-acne/", "label": "Best LED Mask for Acne"}
        ]
    },
    "snow-vs-crest-whitestrips": {
        "cta_links": [
            {"url": "/teeth-whitening/", "label": "Teeth Whitening Reviews →"},
            {"url": "/blog/snow-vs-hismile-teeth-whitening/", "label": "Snow vs HiSmile →"}
        ],
        "related_articles": [
            {"url": "/blog/best-teeth-whitening-sensitive/", "label": "Best Teeth Whitening for Sensitive Teeth"},
            {"url": "/blog/snow-vs-hismile-teeth-whitening/", "label": "Snow vs HiSmile: Which Whitens Faster?"}
        ]
    }
}

def generate_link_injection_html(cluster):
    """Generate the HTML for link injection based on cluster data."""
    cta_links_html = "\n".join([
        f'  <a href="{link["url"]}" style="display:inline-block;background:#2563eb;color:#fff;padding:0.5rem 1rem;border-radius:6px;text-decoration:none;font-weight:600;font-size:0.88rem;margin:0.25rem 0.25rem 0.25rem 0">{link["label"]}</a>'
        for link in cluster["cta_links"]
    ])

    related_articles_html = "\n".join([
        f'    <li><a href="{link["url"]}">{link["label"]}</a></li>'
        for link in cluster["related_articles"]
    ])

    injection = f"""<!-- aesteticadvice-link-injected -->

<div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:1.25rem 1.5rem;margin:2rem 0">
  <strong style="display:block;color:#111827;margin-bottom:0.75rem;">Ready to shop? See our tested picks:</strong>
{cta_links_html}

</div>

<div style="background:#f0f7ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;padding:1.25rem 1.5rem;margin:2rem 0">
  <strong style="display:block;color:#1e3a8a;margin-bottom:0.75rem;font-size:0.9rem;text-transform:uppercase;letter-spacing:0.05em">Related Articles</strong>
  <ul style="list-style:none;margin:0;padding:0">
{related_articles_html}
  </ul>
</div>
"""
    return injection

def has_link_injection(file_path):
    """Check if file already has the link injection marker."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return 'aesteticadvice-link-injected' in content

def inject_links(file_path, cluster_data):
    """Inject links into the blog post HTML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate the injection HTML
    injection_html = generate_link_injection_html(cluster_data)

    # Try to insert before </article> first
    if '</article>' in content:
        content = content.replace('</article>', injection_html + '\n</article>', 1)
    # Otherwise try to insert before </main>
    elif '</main>' in content:
        content = content.replace('</main>', injection_html + '\n</main>', 1)
    # Otherwise insert before </body>
    elif '</body>' in content:
        content = content.replace('</body>', injection_html + '\n</body>', 1)
    else:
        print(f"  WARNING: Could not find insertion point for {file_path}")
        return False

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return True

def main():
    """Main function to process all blog posts."""
    print("Starting internal link injection for AesteticAdvice blog posts...\n")

    results = {
        "success": [],
        "skipped": [],
        "failed": []
    }

    for post_slug, cluster_data in LINK_CLUSTERS.items():
        post_path = os.path.join(BLOG_DIR, post_slug, "index.html")

        if not os.path.exists(post_path):
            print(f"❌ {post_slug}: File not found at {post_path}")
            results["failed"].append(post_slug)
            continue

        if has_link_injection(post_path):
            print(f"⏭️  {post_slug}: Already has link injection, skipping")
            results["skipped"].append(post_slug)
            continue

        try:
            if inject_links(post_path, cluster_data):
                print(f"✅ {post_slug}: Links injected successfully")
                results["success"].append(post_slug)
            else:
                print(f"❌ {post_slug}: Failed to inject links")
                results["failed"].append(post_slug)
        except Exception as e:
            print(f"❌ {post_slug}: Error - {str(e)}")
            results["failed"].append(post_slug)

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Successfully injected: {len(results['success'])}")
    for post in results["success"]:
        print(f"   - {post}")

    if results["skipped"]:
        print(f"\n⏭️  Skipped (already injected): {len(results['skipped'])}")
        for post in results["skipped"]:
            print(f"   - {post}")

    if results["failed"]:
        print(f"\n❌ Failed: {len(results['failed'])}")
        for post in results["failed"]:
            print(f"   - {post}")

    total = len(results["success"]) + len(results["skipped"])
    print(f"\nTotal processed: {total}/{len(LINK_CLUSTERS)}")

if __name__ == "__main__":
    main()

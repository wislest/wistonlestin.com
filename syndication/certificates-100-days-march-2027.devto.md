---
title: In March, TLS certificates drop to 100 days. The ones nobody owns are what break.
published: false
description: The CA/Browser Forum schedule is fixed — a 100-day maximum from 15 March 2027. Renewal cadence doubles, and the certificates that break are the forgotten subdomain and the one whose owner left.
tags: security, devops, sysadmin, ssl
canonical_url: https://wistonlestin.com/posts/certificates-100-days-march-2027
---

The schedule is fixed and public. The part that catches teams out isn't the renewal cadence on the domain they think about every day — it's the certificate issued three years ago by somebody who has since left.

## The schedule

In April 2025 the CA/Browser Forum passed ballot SC-081v3, which sets a staged reduction in how long a publicly trusted TLS certificate may live. It is not a proposal and it is not vendor marketing: it sits in the TLS Baseline Requirements, section 6.3.2, with dates attached.

| From | Maximum certificate lifetime | Domain validation reuse |
|---|---|---|
| 2020 | 398 days | 398 days |
| 15 March 2026 | 200 days *(in force)* | 200 days |
| **15 March 2027** | **100 days** | **100 days** |
| 15 March 2029 | 47 days | 10 days |

Each date applies to certificates issued from that day forward. Anything already issued keeps running until its own expiry, so the change arrives gradually rather than as a cliff. Some CAs shave a day off to stay safely inside the ceiling — DigiCert issues 199 rather than 200, and will issue 99 rather than 100.

Most of the writing about this fixates on the 47-day number. That one lands in 2029 and nobody is going to act on it today. The date worth a calendar entry is **15 March 2027**, which is about five months away.

## What actually changes

At 200 days you renew roughly twice a year. At 100 days you renew roughly four times. If renewal is automated, that is a configuration detail and you will barely notice. If any part of it is manual — a person who generates a CSR, emails it, waits for the signed certificate, and installs it on a box — you have doubled the number of times that person has to not be on vacation.

The domain validation reuse window halves on the same date. Teams who batch their revalidation once or twice a year will be doing it four times, and the reuse period stops covering the gap between renewals the way it used to.

## The failure mode is not the certificate you're thinking of

Ask an IT lead which certificates they have and you usually get the right answer for the main site, the API, and the mail gateway. Those are automated, monitored, or at least remembered. They are not what takes a service down at 2 a.m.

What takes the service down is the long tail:

- a subdomain stood up for a campaign that ended, still resolving, still serving
- an appliance or load balancer with a certificate installed by hand, outside whatever ACME client covers the web tier
- an internal tool that got a publicly trusted certificate because it was easier at the time
- a certificate issued by a team, a contractor, or an employee who is no longer there, and whose renewal nobody inherited

Shorter lifetimes don't create these. They surface them, four times a year instead of once, and with less slack each time. A certificate that was quietly going to break in 2027 now gets three more chances to break first.

The useful property here is that these certificates are not actually hidden. Every publicly trusted certificate issued since 2018 is written to **certificate transparency logs**, which are append-only and public by design. The forgotten subdomain is discoverable from the outside, by you or by anyone else. The organisations that get caught are not the ones with no record — they are the ones who never went and read it.

## What I would do before March

**1. Inventory from the outside, not from the spreadsheet.** Pull your organisation's certificates out of CT logs and compare that list against what your team believes it runs. The delta is the interesting part, and it is usually not empty.

**2. Put a name against every renewal.** Not a team, a person. "Platform owns it" is how a certificate ends up owned by nobody after a reorg.

**3. Automate what ACME can reach.** Web tier, CDN, reverse proxies, most cloud load balancers. This is solved work and there is no reason to carry it by hand into a 100-day cadence.

**4. Monitor what it can't.** Automation is not universal: network appliances, some vendor-managed platforms, anything where a certificate is installed through a vendor console or pinned by a client. Those stay manual for the foreseeable future, which means the only thing standing between them and an outage is somebody noticing in time.

**5. Rehearse now, while the window is still 200 days.** A renewal process you have run twice under no pressure is a different thing from one you first exercise in March.

## Why I care about this one

Most of what I write is about detection: whether a rule fires, whether a metric means anything, whether a system can be proven to work. Certificate expiry sits in the same family and gets far less attention, because it isn't an attack. It is the *silent* failure — nothing is compromised, nobody is breached, and the service is simply down, with a browser warning in front of every customer and a clock that was visible the whole time.

That is the part I find hard to leave alone. The information was public, dated, and machine-readable. The outage still happened because nobody was reading it.

---

*Sources: CA/Browser Forum ballot SC-081v3 (passed 11 April 2025) and the [TLS Baseline Requirements](https://cabforum.org/working-groups/server/baseline-requirements/documents/), sections 6.3.2 and 4.2.1. Disclosure: I build [CertWatch](https://secureorbit.cloud/), a managed certificate monitoring service, which is where my interest in the long tail comes from. Originally published on [my site](https://wistonlestin.com/posts/certificates-100-days-march-2027).*

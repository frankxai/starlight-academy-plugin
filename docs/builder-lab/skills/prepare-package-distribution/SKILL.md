---
name: prepare-package-distribution
description: "Prepare external storefront delivery and channel economics for an agent package, or inspect its release requirements. Use for Polar, Gumroad, Whop and marketplace planning; creates reviewable drafts without changing live commerce."
---

# Prepare package distribution

Read the relevant channel in
[the ecosystem reference](../../distribution.md). Recheck its
current primary documentation. Account-specific pricing, product eligibility,
country support and tax treatment require their own evidence.

Keep storefront checkout separate from an OpenAI directory plugin. As observed
on 2026-10-01, its rules prohibit digital-product sales and upgrade promotion,
including indirect freemium upsells. It can serve existing paid-account features.
Do not add purchase links, pricing pitches or upgrade routing to the plugin.
This educational workflow is not a storefront for this lab.

Prepare an external product draft with the artifact version and hash, buyer
license, file benefit, update period, self-service setup, refund behavior and
channel-specific eligibility. For Polar, prefer managed downloads or GitHub access
before inventing a billing server. License keys can control update access but
cannot prevent copying local skill instructions. Never bundle an admin token.

For a Polar plan, declare every applicable supported `polar_offer_categories`
value described in the ecosystem reference. The 2026-10-03 AUP check flags AI
content-generation tools and eBooks for closer review and refuses declared
third-party resale marketplaces, physical goods, human services and get-rich
schemes. Missing declarations remain unclassified. This is a bounded declaration
check, not product inspection or provider approval: review the full current AUP,
rights and seller context, and retain the actual provider decision where required.
Do not replace a restricted category with `software` to bypass review.

Resolve this external kit's root, then use
`docs/builder-lab/scripts/distribution_lab.py economics INPUT.json` from the
repository root for explicit scenario inputs.
The fixed fee and all monetary inputs must share one currency. Include tax in the
fee base where applicable, retained fees after refunds, affiliate costs, variable
delivery costs, maintenance allocation and acquisition spend. Label the output a
scenario, not a revenue forecast. Do not hardcode an unverified account rate.

Use `docs/builder-lab/scripts/distribution_lab.py plan PRODUCT.json` to draft channel requirements.
Keep checkout unavailable until demand, pricing, host tests, rights review and
independent review meet the owner's release gate. Package checks do not satisfy
that gate. Live product creation, submission, rollout and customer communications
remain distinct actions governed by the user's actual authorization.

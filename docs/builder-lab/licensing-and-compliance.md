# Rights and launch obligations

Research checked 1 October 2026. This is a release review register, not a legal
opinion or a compliance certification. Applicability depends on the actual seller,
buyer, intended use, delivered software and territory. Each applicable row needs
a named human accountable owner and specialist review where unresolved.
Private evidence remains outside this public repository. Shared entity/obligation
work lives in [agentic-ops 77](https://github.com/frankxai/agentic-ops/issues/77).

| Review area | Product-specific evidence before paid launch | Source |
| --- | --- | --- |
| Seller, payout and tax | Actual registered seller and authorized merchant account; accountant confirms VAT/income/reporting allocation; no proposed entity represented as formed | [Dutch online-business guide](https://business.gov.nl/starting-your-business/starting-situations/step-by-step-plan-for-starting-an-online-business/) |
| Merchant of record | Confirm account eligibility, actual fee plan, seller-of-record and refund/dispute responsibilities. Polar handles indirect sales tax on its transactions; verify remaining business obligations separately | [Polar MoR](https://polar.sh/docs/merchant-of-record/introduction) |
| Consumer purchase | Identity, complete price, technical requirements, compatibility, delivery, update/support terms and remedy route; distinguish B2B and B2C | [Dutch distance sales](https://business.gov.nl/regulations/long-distance-sales-and-purchases/) |
| Withdrawal and digital delivery | Evidence of express consent to immediate delivery, acknowledgment of withdrawal consequences and durable confirmation where the exception applies; no blanket no-refund claim removes statutory remedies | [Digital-content cancellation](https://business.gov.nl/regulations/cancellation-period-sale/) |
| Online withdrawal interface | Check actual website/platform implementation and applicability of the cancellation control introduced 19 June 2026; provider screenshots alone do not prove our journey | [Dutch cancellation button](https://business.gov.nl/amendments/online-shops-must-have-cancellation-button/) |
| Personal data and marketing | Purpose/lawful basis, controller/processor roles, minimization, retention, deletion, security, transfers and consent/unsubscribe rules; interest recording is distinct from newsletter consent | [GDPR official text](https://eur-lex.europa.eu/eli/reg/2016/679/oj), [AP direct-marketing objection](https://autoriteitpersoonsgegevens.nl/themas/basis-avg/privacyrechten-avg/recht-van-bezwaar) |
| AI system roles and use | Classify actual provider/deployer activity and intended use; assess prohibited/high-risk scope, applicable transparency and effective dates from current law. A skill package is not automatically a GPAI model | [AI Act scope](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-2), [transparency Article 50](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50) |
| Accessibility | Determine applicable e-commerce/accessibility duties and exemptions; perform keyboard, focus, mobile/touch and reduced-motion journey checks before release | [Dutch web-shop rules](https://business.gov.nl/regulations/long-distance-sales-and-purchases/) |
| Source and asset rights | Exact upstream revision, licence text, notices, modifications, redistribution conditions and commercial rights for every included dependency, template, dataset, font and media file | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), [SPDX licence list](https://spdx.org/licenses/) |
| Lab and channel terms | Exact account/product terms, public-directory rules, branding, permitted scope, data handling and marketplace category eligibility; no implied lab endorsement | [OpenAI plugin policy](https://developers.openai.com/plugins/plugin-guidelines), [channel research](distribution.md) |

Article 50 distinguishes direct AI interaction, provider marking duties, deepfakes
and public-interest text, with conditions and exceptions. It does not establish
a blanket rule that every AI-assisted document needs the same label. Preserve
current sources and record the actual use-case decision. Recheck legal sources
when a product/channel changes and before launch; monthly review is a proposed
cadence, not a substitute for effective-date monitoring.

## Per-package rights inventory

Store a sanitized inventory beside each original package:

```json
{
  "artifact": "relative/path/to/file",
  "origin": "original or exact upstream URL and revision",
  "license_id": "verified SPDX identifier or reviewed proprietary terms",
  "license_text_path": "LICENSES/component.txt",
  "notice_path": "NOTICE when required",
  "modified": false,
  "commercial_redistribution": "unreviewed",
  "reviewer": "unassigned",
  "evidence_ref": "private record ID",
  "review_due": "2026-10-20"
}
```

The scaffold's licence field cannot confer rights the seller does not possess.
Apache-licensed source permits commercial reuse subject to its conditions; a paid
customer retains applicable open-source rights. Do not add a proprietary restriction
that contradicts included licences or promise exclusivity over the free lab. Check
NOTICE obligations, attribution and modified-file notices; copyleft and third-party
media require their own analysis. Host/API output terms, copyright protectability,
trademarks and permission to use other people's material are separate questions.

For an original proprietary domain pack, define permitted users, redistribution,
updates, support duration and product limitations through reviewed terms. A licence
key or download gate grants access and can be revoked in the service; it cannot
erase a downloaded file or override open-source rights. Do not invent lifetime
support, universal compatibility or guaranteed revenue.

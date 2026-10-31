# 0001 Register API keys under PubHealth Commons

Status: Accepted (Andrea King, 2026-10-31)

Context. The Delphi key and the Socrata app token each ask for an organization name.

Decision. Register both under PubHealth Commons.

Consequences. Keys live only in a local `.env` file, never in the repository. The person who registers records the account email in the team's password manager, not here.

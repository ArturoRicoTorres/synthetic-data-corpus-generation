# Internal group role (INTRNL_GRP_RL_IL)

A Internal group role is a role an Internal group may act in.

## Columns

| Column | Business name | Type | Key | Definition |
|---|---|---|---|---|
| `DT_RFRNC` | [Reference date](../../../shared/regulatory/glossary.md#reference-date) | DATE | PK | Reporting agents shall report credit data as recorded on the following reporting reference dates: (a) for monthly transmissions, on the last day of each month; (b) for quarterly transmissions, on the last day of March, June, September and December. |
| `RPRTNG_AGNT_ID` | [Reporting agent identifier](../../../shared/regulatory/glossary.md#reporting-agent-identifier) | VARCHAR(255) | PK | Reporting agent identifier |
| `ACCNTNG_CNSLDTN_LVL` | [Accounting consolidation level](../../../shared/regulatory/glossary.md#accounting-consolidation-level) | VARCHAR(255) | PK | Accounting consolidation level is the level on which the accounting is consolidated, Solo or group. |
| `ACCNTNG_STNDRD` | [Accounting standard](../../../shared/regulatory/glossary.md#accounting-standard) | VARCHAR(255) | PK | Accounting standard |
| `GRP_ID` | [Group ID](../../../shared/regulatory/glossary.md#group-id) | VARCHAR(255) | PK | RIAD Code of the head entity of group concatenated with the type of group, for example DE00001.A (Entity with RIAD Code DE00001 is the head of the Type A group). |
| `GRP_RL_TYP` | [Internal group role type](../../../shared/regulatory/glossary.md#internal-group-role-type) | VARCHAR(255) | PK | A discriminator to distinguish between different roles a group may act in. |
| `FNRP_RPRTNG_SCHM` | [Finrep reporting scheme](../../../shared/regulatory/glossary.md#finrep-reporting-scheme) | VARCHAR(255) |  | Finrep reporting scheme |

## Relationships

Joined to every position on the reporting context: DT_RFRNC, RPRTNG_AGNT_ID, ACCNTNG_CNSLDTN_LVL,
ACCNTNG_STNDRD. Each reporting context has exactly one row with group role type GRP_RL_TYP_1.


## Code lists

### GRP_RL_TYP: Group role type

| Code value | Code | Name |
|---|---|---|
| `GRP_RL_TYP_1` | 1 | Reporting agent internal group role |

### FNRP_RPRTNG_SCHM: Finrep reporting scheme

| Code value | Code | Name |
|---|---|---|
| `FNRP_RPRTNG_SCHM_1` | 1 | Full |
| `FNRP_RPRTNG_SCHM_2` | 2 | Simplified |
| `FNRP_RPRTNG_SCHM_3` | 3 | Over-simplified |

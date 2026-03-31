# Windchill SDK

Python SDK + MCP Server voor PTC Windchill REST API. Maakt Windchill PLM toegankelijk voor Claude Desktop.

## Installatie (Claude Desktop)

1. Pak de zip uit naar een map, bijv. `C:\windchill_sdk`
2. Open een terminal in die map
3. Voer uit:

```
python scripts/install.py
```

4. Vul je Windchill credentials in (worden lokaal opgeslagen)
5. **Herstart Claude Desktop**
6. Vraag Claude: *"Welke containers zijn er in Windchill?"*

## Wat kan je vragen aan Claude?

- "Zoek part WH806239"
- "Toon openstaande change requests"
- "Welke workflow taken staan open?"
- "Download het document van WH806239"
- "Zoek documenten met FD-1460 in de naam"
- "Welke containers zijn er?"

## Verwijderen

```
python scripts/uninstall.py
```

## Veiligheid

- Credentials worden **alleen lokaal** opgeslagen (`.env` + Claude Desktop config)
- De MCP server draait **lokaal op je PC** als een Python process
- Alle Windchill API calls gaan direct van jouw PC naar `plm.contiweb.com` via de VPN
- Credentials verlaten je PC **nooit** - ze worden niet naar Anthropic gestuurd
- Tool results (part data, change requests, etc.) worden wel naar Anthropic gestuurd zodat Claude een antwoord kan formuleren

## Handmatige configuratie

Als het install script niet werkt, kun je de MCP server handmatig configureren.

### 1. SDK installeren

Open een terminal in de map waar je de zip hebt uitgepakt:

```
pip install -e .[mcp]
```

### 2. Claude Desktop configureren

Open het configuratiebestand:

- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Voeg het volgende toe (of maak het bestand aan als het niet bestaat):

```json
{
  "mcpServers": {
    "windchill": {
      "command": "python",
      "args": ["C:\\pad\\naar\\windchill_sdk\\run_mcp.py"],
      "env": {
        "WINDCHILL_BASE_URL": "https://plm.contiweb.com/Windchill/servlet/odata",
        "WINDCHILL_USERNAME": "jouw_gebruikersnaam",
        "WINDCHILL_PASSWORD": "jouw_wachtwoord",
        "WINDCHILL_VERIFY_SSL": "false",
        "WINDCHILL_API_VERSION": "3"
      }
    }
  }
}
```

**Let op:**
- Vervang `C:\\pad\\naar\\windchill_sdk` door het daadwerkelijke pad waar je de bestanden hebt uitgepakt
- Gebruik dubbele backslashes (`\\`) in Windows paden
- Vul je eigen Windchill gebruikersnaam en wachtwoord in
- Als er al andere MCP servers in het bestand staan, voeg `windchill` toe binnen het bestaande `mcpServers` blok

### 3. Launcher script aanmaken

Maak het bestand `run_mcp.py` aan in de hoofdmap van de SDK:

```python
"""Launcher script for the Windchill MCP Server."""
import sys
sys.path.insert(0, r"C:\pad\naar\windchill_sdk\src")
from windchill_mcp.server import main
main()
```

Vervang het pad door je eigen installatiepad.

### 4. Herstart Claude Desktop

Sluit Claude Desktop volledig af en open het opnieuw. De Windchill tools zijn nu beschikbaar.

---

# API Reference

> Complete API reference for PTC Windchill REST Services v1.6 (OData-based).
> Base URL: `https://<server>/Windchill/servlet/odata/`
> Authentication: HTTP Basic Auth or session cookie. CSRF_NONCE required for write operations.

## Quick Start

1. [Accessing Domains](docs/accessing-domains.md) - URL structure and authentication
2. [Domains Overview](docs/domains-overview.md) - All available domains with IDs
3. [Fetch NONCE Token](docs/example-fetch-nonce.md) - Required before any write operation
4. [OData Query Parameters](docs/odata-query-parameters.md) - $filter, $select, $expand, $orderby, $top, $skip

---

## Framework & Architecture

| File | Description |
|------|-------------|
| [Framework Overview](docs/framework-overview.md) | Architecture, configuration-driven design, JavaScript hooks |
| [OData as Service](docs/odata-as-service.md) | Domains as OData services, URL patterns |
| [Entity Data Model](docs/entity-data-model.md) | EDM, $metadata endpoint, CSDL format |
| [OData Primitives](docs/odata-primitives.md) | Supported types: String, Int, Boolean, DateTimeOffset, etc. |
| [Process HTTP Requests](docs/process-http-requests.md) | Request pipeline, Nashorn JS hooks, Windchill Java API access |
| [PTC Annotations](docs/ptc-annotations.md) | PTC.ReadOnly, PTC.Operations, PTC.SecurityLabel, etc. |
| [Inheriting Capabilities](docs/inheriting-capabilities.md) | 20+ capabilities: versioned, workable, lifecycleManaged, contentHolder, etc. |
| [API Catalog](docs/api-catalog.md) | Swagger/API catalog in Windchill UI |

## OData Query & Filtering

| File | Description |
|------|-------------|
| [OData Query Parameters](docs/odata-query-parameters.md) | $filter, $select, $expand, $orderby, $top, $skip, $count |
| [Filter on Navigation Properties](docs/filter-navigation-properties.md) | Lambda expressions, Context/Organization/Folder/Attachments filtering |
| [OrderBy Sorting Options](docs/orderby-sorting-options.md) | Sorting on primitives, complex types, navigation properties |
| [DateTime Offset](docs/datetime-offset.md) | Date filtering syntax and examples |
| [OData Prefer Headers](docs/odata-prefer-headers.md) | odata.maxpagesize, return=representation/minimal |
| [Latest Version Search](docs/latest-version-search.md) | ptc.search.latestversion query option |

## Common Operations

| File | Description |
|------|-------------|
| [CheckIn/CheckOut/Delete](docs/actions-checkin-checkout-delete.md) | Single and bulk operations, atomic behavior |
| [Common Navigation Properties](docs/common-navigation-properties.md) | Creator, Modifier - available in all domains |
| [Lifecycle States](docs/lifecycle-states.md) | GetValidStateTransitions function |
| [Set Lifecycle State](docs/set-lifecycle-state.md) | SetState action |
| [NONCE Token Function](docs/nonce-token-function.md) | CSRF protection for write operations |
| [Error Codes](docs/error-codes.md) | HTTP status codes returned by Windchill REST Services |
| [Batch Support](docs/batch-support-theory.md) | Batch request protocol and theory |
| [Batch Request Examples](docs/batch-request-examples.md) | Simple + advanced batch with Content-ID cross-references |

---

## Domain References

### Core Domains

| File | Domain ID | Description |
|------|-----------|-------------|
| [Product Management](docs/product-management-domain.md) | `ProdMgmt` | Parts, BOM, PartUse, AXL entries |
| [Product Management Actions](docs/prodmgmt-actions-functions.md) | `ProdMgmt` | GetBOM, GetPartStructure, GetPartsList, UpdateCommonProperties |
| [Document Management](docs/document-management-domain.md) | `DocMgmt` | Documents, content upload/download |
| [Document Management Actions](docs/document-management-actions.md) | `DocMgmt` | UpdateCommonProperties for documents |
| [Change Management](docs/change-management-domain.md) | `ChangeMgmt` | ProblemReport, ChangeRequest, ChangeNotice, ChangeTask, Variance |
| [Workflow](docs/workflow-domain.md) | `Workflow` | WorkItems, Activities, completion, reassignment |
| [Workflow Actions](docs/workflow-domain-actions.md) | `Workflow` | CompleteWorkitem, SaveWorkitem, ReassignWorkItems |
| [Workflow Functions](docs/workflow-domain-functions.md) | `Workflow` | GetWorkItemReassignUserList |

### Data & Administration

| File | Domain ID | Description |
|------|-----------|-------------|
| [Data Administration](docs/data-administration-domain.md) | `DataAdmin` | Containers, Folders (CRUD), Products, Libraries, Projects |
| [Principal Management](docs/principal-management-domain.md) | `PrincipalMgmt` | Users, Groups, Organizations, License Groups |
| [Common Domain](docs/common-domain.md) | `PTC` | ContentItem, ApplicationData, URLData, WindchillEntity |
| [Common Domain Functions](docs/common-domain-functions.md) | `PTC` | GetEnumTypeConstraint, GetAllStates, GetWindchillMetaInfo |

### Engineering

| File | Domain ID | Description |
|------|-----------|-------------|
| [CAD Document Management](docs/cad-document-management-domain.md) | `CADDocumentMgmt` | CADDocument, PartAssociation, CADStructure |
| [Manufacturing Process Mgmt](docs/manufacturing-process-management-domain.md) | `MfgProcMgmt` | ProcessPlans, Operations, Sequences, BOP |
| [Classification Structure](docs/classification-structure-domain.md) | `ClfStructure` | ClfNode, ClassifiedObject, classification search |
| [Effectivity Management](docs/effectivity-management-domain.md) | `EffectivityMgmt` | Date/Unit/Block/Serial effectivities |
| [Product Platform Mgmt](docs/product-platform-management-domain.md) | `ProdPlatformMgmt` | Options, Choices, OptionSets, VariantSpecifications |
| [Visualization](docs/visualization-domain.md) | `Visualization` | Representations, Creo View URLs, thumbnails |

### Supply Chain

| File | Domain ID | Description |
|------|-----------|-------------|
| [Supplier Management](docs/supplier-management-domain.md) | `SupplierMgmt` | SourcingContext, AML/AVL entries |

### Quality (requires Quality product)

| File | Domain ID | Description |
|------|-----------|-------------|
| [Quality Management System](docs/quality-management-system-domain.md) | `QMS` | People, Places, Addresses, Subjects |
| [Nonconformance](docs/nonconformance-domain.md) | `NC` | Nonconformance processes |
| [CAPA](docs/capa-domain.md) | `CAPA` | Corrective & Preventive Actions |
| [Customer Experience Mgmt](docs/customer-experience-management-domain.md) | `CEM` | Customer complaints/feedback |

### Other Domains

| File | Domain ID | Description |
|------|-----------|-------------|
| [Saved Search](docs/saved-search-domain.md) | `SavedSearch` | Execute saved searches via API |
| [Event Management](docs/event-management-domain.md) | `EventMgmt` | Webhook subscriptions |
| [PDM (Conglomerate)](docs/pdm-domain.md) | `PDM` | Read-only combined domain for PowerBI/Excel |

---

## Code Examples

### Parts & BOM
| File | Operation |
|------|-----------|
| [Create Part](docs/example-create-part.md) | POST to ProdMgmt/Parts |
| [Checkout Part](docs/example-checkout-part.md) | PTC.ProdMgmt.CheckOut action |
| [Checkin Part](docs/example-checkin-part.md) | PTC.ProdMgmt.CheckIn action |
| [Read BOM](docs/example-read-bom.md) | GetBOM / GetPartStructure with $expand |
| [Create Part Usage Link](docs/example-create-part-usage-link.md) | BOM entry with occurrences |
| [Revise Multiple Parts](docs/example-revise-multiple-parts.md) | Bulk revision |
| [Query with Filter](docs/example-query-filter.md) | $filter examples |

### Documents
| File | Operation |
|------|-----------|
| [Create Document](docs/example-create-document.md) | POST to DocMgmt/Documents |
| [Upload Content](docs/example-upload-content.md) | 3-stage file upload process |

### Workflow
| File | Operation |
|------|-----------|
| [Complete Work Item](docs/example-complete-workitem.md) | CompleteWorkitem with routing/voting |
| [Reassign Work Items](docs/example-reassign-workitems.md) | ReassignWorkItems action |

### Authentication
| File | Operation |
|------|-----------|
| [Fetch NONCE](docs/example-fetch-nonce.md) | GetCSRFToken() function |

### Batch Operations
| File | Operation |
|------|-----------|
| [Batch Requests](docs/batch-request-examples.md) | Multipart batch with cross-references |

---

## Domain Customization

| File | Description |
|------|-------------|
| [Config Paths](docs/config-paths.md) | Configuration file locations |
| [Domain JSON File](docs/domain-json-file.md) | Domain JSON structure |
| [Create New Domain](docs/create-new-domain.md) | Creating custom domains |
| [Extending Domains](docs/extending-domains.md) | Adding to existing PTC domains |
| [Add Custom Properties](docs/add-custom-properties.md) | Custom properties on entities |
| [Add New Actions](docs/add-new-actions.md) | Custom actions |
| [Add New Functions](docs/add-new-functions.md) | Custom functions |
| [Example: Create Domain](docs/example-create-domain.md) | Full domain creation example |
| [Example: Soft Type](docs/example-soft-type.md) | Extending ProdMgmt with soft type |

---

## Changelogs

| File | Version |
|------|---------|
| [v1.6](docs/changelog-v1.6.md) | Effectivity, PDM domain, ChangeTask, webhooks, pagination |
| [v1.5](docs/changelog-v1.5.md) | API Catalog, Workflow domain, Regulatory Master, security labels |
| [v1.4](docs/changelog-v1.4.md) | Multi-object CRUD, Options & Variants, CAD/Event/Supplier domains |
| [v1.3](docs/changelog-v1.3.md) | Batch refs, classification, Parts List/Visualization/Audit domains |
| [v1.2](docs/changelog-v1.2.md) | MPM, Change Mgmt, Classification, Saved Search domains |
| [v1.1](docs/changelog-v1.1.md) | Dynamic Doc, Quality, Info*Engine, Factory domains |

---

*Source: PTC Windchill REST Services v1.6 Documentation*
*Generated: 2026-03-30*

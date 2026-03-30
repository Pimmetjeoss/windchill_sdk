# PTC Event Management Domain

> **Domain ID:** `EventMgmt`
> **Base URL:** `/Windchill/servlet/odata/EventMgmt`
> **Metadata URL:** `/Windchill/servlet/odata/EventMgmt/$metadata`
> **Added in:** Windchill REST Services 1.4

The PTC Event Management domain provides access to the webhook subscription capabilities of Windchill. Webhook subscriptions enable Windchill to send event notifications to external systems when certain events or actions occur on an object, folder, or context in Windchill through a webhook URL. The domain must be used along with webhooks to subscribe to events.

## Important Limitations

- Webhook subscription is **not** supported for Windchill soft types.
- Subscription to events is supported only for entities available in the following domains:
  - PTC Product Management domain (`ProdMgmt`)
  - PTC Document Management domain (`DocMgmt`)
  - PTC Data Administration domain (`DataAdmin`)
  - PTC Change Management domain (`ChangeMgmt`)
  - PTC NC (Nonconformance) domain (added in v1.5)
  - PTC CAPA domain (added in v1.5)
  - PTC Customer Experience Management (CEM) domain (added in v1.5)
  - PTC CAD Document Management domain (`CADDocMgmt`) (added in v1.6)
  - PTC Service Information Management domain (`ServiceInfoMgmt`) (added in v1.6)
  - PTC Parts List Management domain (`PartsListMgmt`) (added in v1.6)
  - PTC Dynamic Document Management domain (`DynamicDocMgmt`) (added in v1.6)

## Entities

| Item | OData Entity | Description |
|------|-------------|-------------|
| Event subscription | `EventSubscription` | Represents a subscription to an event. Specify the URL to the external system in the `CallbackURL` property. Notifications are sent to this URL. Use POST to create, DELETE to remove. |
| Events | `Event` | Represents the Windchill events to which you can subscribe. |
| Object instance subscription | `EntityEventSubscription` | Represents subscription to events on a specific Windchill object instance. Has `SubscribedOnEntity` navigation property. |
| Container subscription | `EntityTypeInContainerEventSubscription` | Represents subscription to events on a type of Windchill object in a specified context (e.g., a product or library). Has `SubscribedOnContext` navigation property. |
| Folder subscription | `EntityTypeInFolderEventSubscription` | Represents subscription to events on a type of Windchill object in a specified folder. Has `SubscribedOnFolder` navigation property. |

## Entity Sets

| Entity Set | Description |
|-----------|-------------|
| `EventSubscriptions` | Collection of event subscriptions |
| `Events` | Collection of available events |

## Navigation Properties

### On EventSubscription

| Navigation Property | Description |
|--------------------|-------------|
| `SubscribedEvent` | The event being subscribed to |

### On EntityEventSubscription

| Navigation Property | Description |
|--------------------|-------------|
| `SubscribedOnEntity` | The entity instance for the subscription |
| `SubscribedEvent` | The event being subscribed to |

### On EntityTypeInContainerEventSubscription

| Navigation Property | Description |
|--------------------|-------------|
| `SubscribedOnContext` | The container context of the subscription |
| `SubscribedEvent` | The event being subscribed to |

### On EntityTypeInFolderEventSubscription

| Navigation Property | Description |
|--------------------|-------------|
| `SubscribedOnFolder` | The folder context of the subscription |
| `SubscribedEvent` | The event being subscribed to |

## Key URLs

### Subscribe to an Event on a Windchill Object Instance

```http
POST /Windchill/servlet/odata/EventMgmt/EventSubscriptions HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Name": "TestSubscriptionForDoc",
  "CallbackURL": "https://windchill.ptc.com/Windchill",
  "SubscribedEvent@odata.bind": "Events('CHANGE_LIFECYCLE_STATE')",
  "LifeCycleState": {
    "Value": "RELEASED"
  },
  "SubscribedOnEntity@odata.bind": "WindchillEntities('OR:wt.doc.WTDocument:4326293')",
  "SubscribeAllVersions": true,
  "@odata.type": "PTC.EventMgmt.EntityEventSubscription"
}
```

### Subscribe to an Event on a Windchill Object Type in a Container

```http
POST /Windchill/servlet/odata/EventMgmt/EventSubscriptions HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Name": "TestContainerSubscription",
  "CallbackURL": "https://windchill.ptc.com/Windchill",
  "SubscribedEvent@odata.bind": "Events('EDIT_IDENTITY')",
  "SubscribedOnEntityType": "PTC.DocMgmt.Document",
  "ExpirationDate": "2018-12-20T11:30:00Z",
  "SubscribedOnContext@odata.bind": "Containers('OR:wt.pdmlink.PDMLinkProduct:79638')",
  "@odata.type": "PTC.EventMgmt.EntityTypeInContainerEventSubscription"
}
```

### Subscribe to an Event on a Windchill Object Type in a Folder

```http
POST /Windchill/servlet/odata/EventMgmt/EventSubscriptions HTTP/1.1
Content-Type: application/json
CSRF_NONCE: <nonce_value>
```

Request Body:
```json
{
  "Name": "TestFolderSubscription",
  "CallbackURL": "https://windchill.ptc.com/Windchill",
  "SubscribedOnEntityType": "PTC.DocMgmt.Document",
  "ExpirationDate": "2018-12-20T11:30:00Z",
  "SubscribedEvent@odata.bind": "Events('EDIT_ATTRIBUTES')",
  "SubscribedOnFolder@odata.bind": "Folders('OR:wt.folder.SubFolder:5012381')",
  "@odata.type": "PTC.EventMgmt.EntityTypeInFolderEventSubscription"
}
```

### Delete a Subscription

```http
DELETE /Windchill/servlet/odata/EventMgmt/EventSubscriptions('OR:wt.notify.NotificationSubscription:5012541') HTTP/1.1
```

## GetApplicableEvents Function

The `GetApplicableEvents` function returns a list of all events available for subscription for the specified Windchill object type.

**Type:** Unbound function

### Request

```
GET /Windchill/servlet/odata/EventMgmt/GetApplicableEvents(EntityName='PTC.ProdMgmt.Part')
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `EntityName` | `String` | Yes | Windchill object type in the format `PTC.<Domain_Name>.<Entity_Type>` |

### Example Entity Names

| Entity | EntityName |
|--------|-----------|
| Part | `PTC.ProdMgmt.Part` |
| Document | `PTC.DocMgmt.Document` |
| Change Request | `PTC.ChangeMgmt.ChangeRequest` |
| Change Notice | `PTC.ChangeMgmt.ChangeNotice` |

## Common Event Types

Events available for subscription include:

| Event | Description |
|-------|-------------|
| `CHANGE_LIFECYCLE_STATE` | Triggered when an object's lifecycle state changes |
| `EDIT_IDENTITY` | Triggered when an object's identity is edited |
| `EDIT_ATTRIBUTES` | Triggered when an object's attributes are edited |

## EventSubscription Properties

| Property | Type | Description |
|----------|------|-------------|
| `Name` | `Edm.String` | Name of the subscription |
| `CallbackURL` | `Edm.String` | URL to which event notifications are sent |
| `SubscribedOnEntityType` | `Edm.String` | OData entity type (e.g., `PTC.DocMgmt.Document`) |
| `ExpirationDate` | `Edm.DateTimeOffset` | When the subscription expires |
| `SubscribeAllVersions` | `Edm.Boolean` | Whether to subscribe to all versions of the object |
| `LifeCycleState` | `EnumType` | Optional lifecycle state filter |
| `@odata.type` | `String` | Discriminator for subscription type |

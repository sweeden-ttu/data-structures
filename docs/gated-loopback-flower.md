# Gated Loopback Flower (Blossoming Source Root)

Numeric fields (timestamps, counts, indices) follow the **IEEE 752 64-bit geometrica Z field (zed)** specifications. See [IEEE_752_64BIT_GEOMETRICA_Z_FIELD_ZED_SPECIFICATIONS.md](IEEE_752_64BIT_GEOMETRICA_Z_FIELD_ZED_SPECIFICATIONS.md).

## 1) Purpose
The **Gated Loopback Flower (GLF)** is a directed, rooted, multi-branch reference structure for URL-domain traversal and composition.

It supports:
- A canonical **root source domain URL**.
- Child growth where each child can:
  - point to a new root node (**new domain root**), or
  - point to a non-root child node (**in-branch expansion**).
- A **loopback gate** that prevents:
  - cycles back to ancestors,
  - cross-branch re-rooting to nodes already rooted in another branch.

This makes GLF safe for crawling, trust-graph expansion, lineage analysis, and federated source indexing.

## 2) Core Concepts

### Node Types
- **ROOT**: primary domain root in a flower graph.
- **CHILD**: non-root node attached under a root/child lineage.
- **REFERENCE**: lightweight edge target reference, used for projected or deferred expansion.


### Node identity encoding rules
1. **Primary node identity**: each node has a unique two-character hexadecimal identifier `hh`, constrained to global identity space `0x00..0x63` (limit `0x64` slots) across all roots.
2. **Extended lineage identity**: node identity may be clarified as:
   - `hh` + first three single characters of ancestor nodes in traversal order + first two hex chars of root identifier (if root is not null).
3. **Canonical identity fields**:
   - `node_hex_id` (required): two-char hex unique within global identity space.
   - `lineage_suffix` (optional): concatenated three-char ancestor initials.
   - `root_hex_prefix` (optional): first two hex chars of root id, omitted when root is null.
   - `canonical_node_identity` (derived): `node_hex_id + lineage_suffix + root_hex_prefix`.
4. **Global identity space cap**: node identity allocation across all roots is limited to `0x64` total hex-space positions (0x00-0x63).

### Edge Kinds
- **NEW_ROOT**: creates/link-binds to a different root domain graph (federated bloom).
- **NEW_CHILD**: creates/link-binds to a new child in same branch lineage.
- **ALIAS**: non-owning pointer to an existing node (must pass loopback gate rules).

### Gate Invariants (Loopback Prevention)
1. **No ancestor back-edge**: node cannot point to itself or any ancestor.
2. **No duplicate branch rooting**: once a child is rooted under branch A as a rooted reference, it cannot be rooted again under branch B unless marked shared and passing ownership policy.
3. **Canonical root ownership**: every node has one `origin_root_id`.
4. **Monotonic visitation stamp**: traversal tokens are unique per expansion epoch to prevent repeated same-path expansion.


### Associativity notation encoding
- `associativity_notation` must be one of:
  - `---` for **one-to-many** association.
  - `--+*` for **one-to-one** association.
- This notation is descriptive metadata for lawful association semantics and does not replace gate rules.

### Algebraic invariants (required)
1. **Identity closure (all structures)**: every structure defines an identity element and remains closed under its composition operation.
2. **Associativity (collection structures)**: node/edge collection composition must be associative.
3. **Inverse (collection structures)**: each collection operation defines an inverse operation for rollback/reconciliation semantics.


### Immutability and operation mode invariants
1. **Immutable-by-version**: persisted snapshots are append-only; updates create new version IDs.
2. **Dual operation mode**: every payload may be processed as:
   - **STREAM**: incremental append/verify pipeline, or
   - **BLOCK**: fully materialized snapshot for archival/replay.
3. **Cousin/sibling linkage semantics**:
   - `sibling_status` indicates whether same-parent branch state is OPEN, STABLE, or SEALED.
   - `cousin_pointer` references logically associated branch/version for associativity/inverse reconciliation.
4. **Safe-to-stream rule**: stream continuation is allowed only when sibling/cousin constraints pass gate policy and no inverse conflict is pending.
5. **Safe-to-store rule**: block persistence is allowed when URL and ancestor chain have passed validation + verification in current epoch.

### Storage-at-rest cryptographic policy
1. **Encrypted at rest by default**: each structure and ancestor lineage is stored encrypted before validation.
2. **Decrypt only for validation/verification**: plaintext exposure is restricted to active verification windows.
3. **Post-verification cleartext materialization**: once URL and all ancestors are validated/verified, both structure and ancestors are stored in clear text as trusted materialized state.
4. **Audit requirement**: transitions encrypted -> decrypted -> cleartext must produce immutable audit events.


### Anchor, ancestor, and validator/verifier role policy
1. **Anchor permanence**: once a structure is validated and verified, it becomes an `ANCHOR` and must never be encrypted again.
2. **Root as mandatory anchor**: the root structure is always an `ANCHOR` and is blocked from invoking or applying encryption methods to itself.
3. **Anchor capability scope**: anchors may perform encryption tasks on non-anchor descendants/ancestors, but anchor payload state remains cleartext.
4. **Ancestor flexibility**: non-anchor ancestors may be encrypted or decrypted as required by policy and workflow.
5. **Validator/verifier authority**: validator/verifier roles may:
   - convert eligible ancestors into anchors after successful validation+verification,
   - encrypt/decrypt non-anchor ancestors,
   - execute cross-branch traversal for lineage verification.
6. **No-anchor-regression rule**: state transitions from `ANCHOR` back to encrypted states are forbidden.


### Remote blossom-save and synchronization safety policy
1. **Remote full-trie save action**: when saving an entire trie/blossom to any remote copy, invoke `AES_ENCRYPT_AND_STORE` on all remote targets.
2. **Processing shutdown requirement**: after remote encrypt-and-store starts, stop further processing and terminate unresponsive processes after 60 seconds.
3. **Pre-sync gating**: synchronization may only be attempted after the remote save-shutdown sequence completes.
4. **Dirty encryption divergence rule**: if corresponding tries disagree on encrypted state for any matched node (encrypted on one remote trie and not the other), both tries are marked `DIRTY_ENCRYPTION_DIVERGENCE` and are ineligible for sync.
5. **Dirty-state allowed actions only**: when dirty, no mutation, traversal expansion, merge, or reconciliation actions are permitted.
6. **Dirty-state required actions**: the only allowed action is to save the AES-encrypted serializable structure to disk, shutdown all processes, and notify all agents of pending shutdown.

## 3) Abstract Data Model (language neutral)

### Primary structures
- `FlowerGraph`
  - `graph_id: UUID`
  - `root_node_id: NodeID`
  - `nodes: Map<NodeID, Node>`
  - `edges: Map<EdgeID, Edge>`
  - `gate_policy: GatePolicy`
  - `algebraic_laws: AlgebraicLaws`
  - `immutability_policy: ImmutabilityPolicy`
  - `storage_policy: StoragePolicy`
  - `role_policy: RolePolicy`
  - `remote_sync_policy: RemoteSyncPolicy`

- `Node`
  - `node_id: NodeID`
  - `node_type: ROOT | CHILD | REFERENCE`
  - `url: URL`
  - `domain_fingerprint: bytes`
  - `origin_root_id: NodeID`
  - `metadata: Map<string, Any>`
  - `node_hex_id: Hex2(0x00..0x63)`
  - `lineage_suffix: string | null`
  - `root_hex_prefix: Hex2 | null`
  - `canonical_node_identity: string`

- `Edge`
  - `edge_id: EdgeID`
  - `from_node_id: NodeID`
  - `to_node_id: NodeID`
  - `kind: NEW_ROOT | NEW_CHILD | ALIAS`
  - `created_at_epoch_ms: uint64`
  - `gate_signature: bytes`

- `GatePolicy`
  - `allow_shared_root_alias: bool`
  - `max_depth: uint32`
  - `max_branch_factor: uint32`
  - `cycle_detection: DFS_COLOR | VISIT_STAMP | TOPO_CACHE`
  - `global_identity_hex_space_limit: uint32` (=0x64)

- `VisitLedger`
  - `epoch_id: UUID`
  - `seen_path_hashes: Set<Hash128>`
  - `root_claims: Map<NodeID, NodeID>` (node -> owning root)

- `AlgebraicLaws`
  - `identity_closure: bool` (must be true)
  - `collections: CollectionLaws`

- `CollectionLaws`
  - `associativity: bool` (must be true)
  - `associativity_notation: --- | --+*`
  - `inverse: bool` (must be true)


- `ImmutabilityPolicy`
  - `immutable_by_version: bool` (must be true)
  - `operation_mode: STREAM | BLOCK`
  - `sibling_status: OPEN | STABLE | SEALED`
  - `cousin_pointer: NodeID | VersionID | null`
  - `safe_to_stream: bool`

- `StoragePolicy`
  - `encrypted_at_rest: bool` (must be true pre-verification)
  - `decrypt_only_for_validation: bool` (must be true)
  - `store_cleartext_after_verified: bool` (must be true)
  - `ancestor_verification_required: bool` (must be true)
  - `audit_transition_events: bool` (must be true)
  - `anchor_never_encrypt: bool` (must be true)
  - `root_is_anchor: bool` (must be true)
  - `root_encryption_blocked: bool` (must be true)


- `RolePolicy`
  - `node_role: ROOT | ANCHOR | ANCESTOR | VALIDATOR | VERIFIER`
  - `can_encrypt_self: bool`
  - `can_decrypt_self: bool`
  - `can_encrypt_others: bool`
  - `can_decrypt_others: bool`
  - `can_promote_to_anchor: bool`
  - `can_cross_branch_traverse: bool`

- Role constraints
  - `ROOT`: `node_role=ANCHOR`, `can_encrypt_self=false`, `can_decrypt_self=false`.
  - `ANCHOR`: `can_encrypt_self=false`, `can_decrypt_self=false`; may encrypt others per policy.
  - `ANCESTOR`: encryption/decryption allowed unless promoted to anchor.
  - `VALIDATOR`/`VERIFIER`: may validate lineage, encrypt/decrypt eligible ancestors, and promote verified ancestors to anchors.

- `RemoteSyncPolicy`
  - `remote_save_mode: AES_ENCRYPT_AND_STORE`
  - `shutdown_unresponsive_after_seconds: uint32` (=60)
  - `block_processing_during_remote_save: bool` (must be true)
  - `sync_requires_remote_save_complete: bool` (must be true)
  - `encrypted_state_mismatch_marks_dirty: bool` (must be true)
  - `dirty_blocks_sync: bool` (must be true)
  - `dirty_allowed_actions: SAVE_AES_TO_DISK | SHUTDOWN_ALL_PROCESSES | NOTIFY_AGENTS_PENDING_SHUTDOWN`

## 4) Baseline Algorithms (implementation guidance)

> Note: these are algorithmic definitions, not schema content.

### 4.1 InsertChild(parent, candidate, edgeKind)
1. Validate node/URL normalization.
2. Compute candidate `path_hash = H(root, ancestry, candidate.url)`.
3. Gate checks:
   - reject if candidate in ancestor set.
   - reject if `root_claims[candidate.node_id]` exists and differs from current root unless policy allows shared alias.
   - reject if `path_hash` already in `seen_path_hashes`.
4. Insert node/edge.
5. Update `seen_path_hashes` and `root_claims`.

Complexity target:
- Average `O(1)` hash checks + `O(h)` ancestor check (`h = depth`), improved to amortized near `O(1)` with ancestor bloom filters.

### 4.2 FederatedRootBloom(fromRoot, externalRootURL)
1. Normalize external root URL.
2. Lookup/create root node with unique domain fingerprint.
3. Create `NEW_ROOT` edge from source branch.
4. Record ownership and gate signature.

Complexity target:
- `O(1)` expected insertion with hash index, `O(log n)` when using ordered map + persistence.

### 4.3 SafeTraversal(root, policy)
- DFS/BFS hybrid with visit-stamps and branch throttling.
- Stop conditions: depth, branch factor, edge policy filter.
- Emits topologically safe expansion stream.

### 4.4 Composition/Reconciliation laws
- Compose operation over collections must satisfy:
  - identity closure: `compose(C, I) = C`
  - associativity: `compose(A, compose(B, C)) = compose(compose(A, B), C)`
  - inverse: `compose(C, inverse(C)) = I`
- `inverse` is semantic (rollback/removal/reconciliation), not necessarily set-theoretic negation.


### 4.5 Stream/Block state machine and storage transitions
- Pre-verify state: `encrypted_at_rest=true`; allow decrypt only for verification routine.
- Verify(URL, ancestors): decrypt working set -> validate URL canonical form + ancestor chain.
- If verify success:
  - emit `VerificationPassed`
  - set `safe_to_stream` per sibling/cousin status gates
  - materialize trusted cleartext snapshot for structure + verified ancestors
- If verify failure:
  - keep encrypted state, emit inverse/reject event, block further stream appends for impacted branch.


### 4.6 Anchor promotion and encryption authority flow
- On `ValidationVerified(node, ancestors)`:
  1. mark `node` as `ANCHOR`; set `anchor_never_encrypt=true` for that lineage record.
  2. if `node` is root, enforce `root_is_anchor=true` and `root_encryption_blocked=true`.
  3. disallow any future encrypt-self operation on anchor/root nodes.
- Validators/verifiers may run cross-branch traversal to confirm ancestor status before promotion.
- Ancestors not yet promoted may be encrypted/decrypted according to storage policy and gate constraints.


### 4.7 Remote AES save, timeout shutdown, and dirty-sync lock
- On `SaveBlossomRemote(all_remotes)`:
  1. execute `AES_ENCRYPT_AND_STORE` for each remote copy.
  2. immediately block further processing for the blossom.
  3. wait for shutdown acknowledgements; kill unresponsive processes at +60s.
  4. notify all agents: `PENDING_SHUTDOWN_REMOTE_ENCRYPTED_SAVE`.
- On `SyncAttempt(trieA, trieB)`:
  - if encrypted-state mismatch on any paired node, mark both `DIRTY_ENCRYPTION_DIVERGENCE` and abort sync.
  - while dirty, only perform: save AES-encrypted serializable payload to disk, shutdown processes, notify agents.

## 5) Performance optimization hints

### CPU + memory
- Use compact integer IDs (`u32`/`u64`) instead of string map keys in hot paths.
- Store edge arrays in SoA layout (`from[]`, `to[]`, `kind[]`) for cache locality.
- Keep URL canonicalization results interned.
- Use lock-free ring buffer for traversal queues in multi-threaded ingest.

### LLVM-oriented notes
- Prefer monomorphized generic containers in Rust/C++ to enable inlining + vectorization.
- Add branch prediction hints for gate rejection hot path.
- Use PGO/LTO for traversal-heavy workloads.
- Avoid virtual dispatch in tight cycle-detection loops.

### GPU / accelerator notes (CUDA, AMD ROCm, Intel oneAPI, Apple Metal)
- Batch gate checks as vectorized kernels over candidate edges.
- Keep adjacency indices in contiguous buffers for coalesced memory reads.
- Use GPU primarily for massive frontier filtering and hash-based duplicate screening.
- Keep host-device transfers amortized via chunked epochs.

### Matrix multiplication adjacency use-cases
When using adjacency matrices for dense subgraphs:
- Use blocked sparse/dense hybrid multiplication.
- Prefer vendor BLAS:
  - NVIDIA cuBLAS/cuSPARSE,
  - AMD rocBLAS/hipSPARSE,
  - Intel MKL/oneMKL,
  - Apple Accelerate/Metal Performance Shaders.
- Maintain bitset masks for gate constraints before matrix kernels to reduce compute.

## 6) Memory and garbage collection guidance

### GC languages (Java/C#/Go/JS)
- Keep graph nodes strongly referenced only from graph registry.
- Use weak references for optional alias caches and reverse lookups.
- Periodically compact tombstoned edges.
- Avoid retaining traversal closures that capture large node maps.

### Manual/ARC ecosystems (C/C++/Rust/Swift)
- Use arena allocators for short-lived traversal epochs.
- Use ref-counted handles for shared aliases; detect cycles via explicit ownership graph, not pure RC.
- Recycle edge blocks with slab allocators.

## 7) Language mapping guidance

### Object-oriented mapping
- Classes: `FlowerGraph`, `Node`, `Edge`, `GatePolicy`, `VisitLedger`, `AlgebraicLaws`, `CollectionLaws`.
- Interfaces:
  - `GateEvaluator`
  - `TraversalStrategy`
  - `OwnershipResolver`
  - `CollectionComposer`

### Functional mapping
- Persistent map/set structures for immutable snapshots.
- Event-sourced updates: `GraphEvent = NodeAdded | EdgeAdded | GateRejected`.
- Traversal as lazy stream/iterator.
- Define lawful monoidal/group-like collection operations for composition + inverse rollback.

### Typed/untyped compatibility
- Typed: generate from Protobuf/JSON Schema/Avro.
- Untyped: validate payloads at API boundary, then normalize to canonical internal form.

## 8) Safety and correctness checklist
- URL canonicalization tested.
- Ancestry gate tests (direct + transitive).
- Cross-branch root-claim collision tests.
- Deterministic traversal order option for reproducibility.
- Schema backward compatibility rules documented.
- Identity-closure, associativity, inverse property tests for collection operations.
- Node identity tests: unique two-char hex id, canonical lineage identity construction, and root prefix handling when root is null/non-null.
- Node identity-space cap tests: enforce 0x64 global slots (0x00-0x63) across all roots.
- Associativity notation tests for `---` (one-to-many) and `--+*` (one-to-one).
- Encrypted-at-rest, decrypt-for-verify-only, and post-verify cleartext materialization tests (including ancestors).
- Anchor permanence tests: root always anchor, no anchor re-encryption, validator/verifier promotion and cross-branch traversal authorization tests.

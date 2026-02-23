from dataclasses import dataclass
from typing import Dict, List, Optional
from threading import RLock


@dataclass
class AnchorNode:
    id: str
    is_stream: bool
    ancestors: List[str]
    machine_anchor: str


class AnchorTree:
    def __init__(self) -> None:
        self._nodes: Dict[str, AnchorNode] = {}
        self._lock = RLock()
        self._initialize()
        self._root = self._nodes.get("C2")

    def _initialize(self) -> None:
        nodes_data = [
            ("C2", False, ["3F", "C2E4", "C2E5", "C2E6", "C2E7"]),
            ("3F", True, ["3FE", "3F8", "3FC"]),
            ("3FE", False, ["C2E40", "C2E41"]),
            ("3F8", True, ["C2E42", "C2E43"]),
            ("3FC", False, ["C2E44"]),
            ("C2E4", False, ["C2E40", "C2E41", "C2E42"]),
            ("C2E5", False, ["C2E50"]),
            ("C2E6", False, ["C2E60"]),
            ("C2E7", False, ["C2E70"]),
            ("C2E40", False, []),
            ("C2E41", False, []),
            ("C2E42", False, []),
            ("C2E43", False, []),
            ("C2E44", False, []),
            ("C2E50", False, []),
            ("C2E60", False, []),
            ("C2E70", False, []),
        ]

        for node_id, is_stream, ancestors in nodes_data:
            self._nodes[node_id] = AnchorNode(
                id=node_id,
                is_stream=is_stream,
                ancestors=ancestors,
                machine_anchor="e4:b9:7a:f8:95:1b",
            )

    @property
    def root(self) -> Optional[AnchorNode]:
        with self._lock:
            return self._root

    def get_node(self, node_id: str) -> Optional[AnchorNode]:
        with self._lock:
            return self._nodes.get(node_id)

    def get_stream_nodes(self) -> List[AnchorNode]:
        with self._lock:
            return [node for node in self._nodes.values() if node.is_stream]

    def get_ancestors(self, node_id: str) -> List[str]:
        with self._lock:
            node = self._nodes.get(node_id)
            return list(node.ancestors) if node else []

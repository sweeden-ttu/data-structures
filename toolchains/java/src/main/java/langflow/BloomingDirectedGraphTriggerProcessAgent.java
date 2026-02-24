package langflow;

/**
 * Blooming-directed-graph trigger process agent (LangFlow namespace: flow/trigger).
 * Triggers the appropriate process across languages, projects, repositories, clusters, and models.
 */
public class BloomingDirectedGraphTriggerProcessAgent {

    public enum Action { GITHUB, HPCC, LOCAL }

    public static Action actionForKey(String contextKey) {
        if (contextKey == null || contextKey.isEmpty()) return Action.LOCAL;
        if (contextKey.contains("github")) return Action.GITHUB;
        if (contextKey.contains("hpcc")) return Action.HPCC;
        return Action.LOCAL;
    }

    public static String resolveContextKey(String cluster, String model, String project) {
        if (cluster == null || model == null) return null;
        String env = "owner_github";
        if (cluster.toLowerCase().contains("hpcc")) {
            env = (project != null && project.toLowerCase().startsWith("owner")) ? "owner_hpcc" : "quay_hpcc";
        } else if (cluster.toLowerCase().contains("github")) {
            env = (project != null && project.toLowerCase().startsWith("hpcc")) ? "hpcc_github" : "owner_github";
        }
        String mod = switch ((model == null ? "" : model).toLowerCase()) {
            case "deepseek" -> "deepseek";
            case "qwen" -> "qwen";
            case "codellama" -> "codellama";
            default -> "granite";
        };
        return env + "_" + mod;
    }
}

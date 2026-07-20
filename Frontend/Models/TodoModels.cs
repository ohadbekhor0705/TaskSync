namespace TodoModels;
public class TodoModel {
    [System.Text.Json.Serialization.JsonPropertyName("title")]
    public string title { get; set; } = string.Empty;
    [System.Text.Json.Serialization.JsonPropertyName("status")]
    public TodoStatus status { get; set; } = TodoStatus.pending;
    [System.Text.Json.Serialization.JsonPropertyName("id")]
    public int id { get; set; }
}
public enum TodoStatus {
    pending,
    completed,
    in_progress
}
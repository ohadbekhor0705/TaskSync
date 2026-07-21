using System.Text.Json.Serialization;

namespace TodoModels;
public class TodoModel {
    [System.Text.Json.Serialization.JsonPropertyName("title")]
    public string Title { get; set; } = string.Empty;
    
    [System.Text.Json.Serialization.JsonPropertyName("status")]
    public TodoStatus Status { get; set; } = TodoStatus.pending;
    [System.Text.Json.Serialization.JsonPropertyName("id")]
    public int Id { get; set; }
}
[JsonConverter(typeof(JsonStringEnumConverter))]
public enum TodoStatus {
    pending,
    completed,
    in_progress
}
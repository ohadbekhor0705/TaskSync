using System.Text.Json.Serialization;
using System.ComponentModel.DataAnnotations;
namespace TodoModels;
public class TodoModel {
    [Required(ErrorMessage = "Title is required.")]
    [StringLength(20, MinimumLength = 3, ErrorMessage = "Title must be between 3 and 20 characters.")]
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
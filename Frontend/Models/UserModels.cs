using System.Text.Json.Serialization;

namespace UserModels {
    public class UserBase {
        public string? username {get; set;}
        public string? email {get; set;}
    }
    public class UserRead : UserBase {
        public int id {get; set;}
    }
    public class LoginResponse
    {
        [JsonPropertyName("access_token")]
        public string? AccessToken { get; set; }
    
        [JsonPropertyName("token_type")]
        public string? TokenType { get; set; }
    
        [JsonPropertyName("user")]
        public UserRead? User { get; set; }
        [JsonPropertyName("message")]
        public string? message { get; set; }
    }
}
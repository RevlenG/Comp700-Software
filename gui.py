import tkinter
import tkinter.messagebox
import customtkinter
import implementation

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Clustering Reviews")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
       
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create the main input panel
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.main_frame.grid(row=0, column=0, padx=(20, 20), sticky="w")

        self.label_path = customtkinter.CTkLabel(self.main_frame, 
                                              text="Enter Dataset Path/Directory: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_path.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.entry_path = customtkinter.CTkEntry(self.main_frame, placeholder_text="c://...", width=200)
        self.entry_path.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

        self.label_tweet = customtkinter.CTkLabel(self.main_frame, 
                                              text="Enter Text/Tweet Column Name: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_tweet.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.entry_tweet = customtkinter.CTkEntry(self.main_frame, placeholder_text="Tweets", width=200)
        self.entry_tweet.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")
        
        self.label_company = customtkinter.CTkLabel(self.main_frame, 
                                              text="Enter Company Column Name: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_company.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.entry_company = customtkinter.CTkEntry(self.main_frame, placeholder_text="Leave blank", width=200)
        self.entry_company.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")

        self.label_sentiment = customtkinter.CTkLabel(self.main_frame, 
                                              text="Enter Sentiment Column Name: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_sentiment.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.entry_sentiment = customtkinter.CTkEntry(self.main_frame, placeholder_text="Sentiment", width=200)
        self.entry_sentiment.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

        self.radio_group_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=5)
        self.radio_group_frame.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(self.radio_group_frame, text="Clustering Method:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_radio_group.grid(row=0, column=1, padx=(20, 20), pady=(5, 5), sticky="nsew")
        self.radio_button_k_means = customtkinter.CTkRadioButton(self.radio_group_frame, text="K-Means Clustering", variable=self.radio_var, value=0)
        self.radio_button_k_means.grid(row=1, column=0, padx=(20, 20), pady=(5, 10), sticky="n")
        self.radio_button_hierarchical = customtkinter.CTkRadioButton(self.radio_group_frame, text="Heirarchical Clustering", variable=self.radio_var, value=1)
        self.radio_button_hierarchical.grid(row=1, column=1, padx=(20, 20), pady=(5, 10), sticky="n")
        self.radio_button_dbscan = customtkinter.CTkRadioButton(self.radio_group_frame, text="DBSCAN Clustering", variable=self.radio_var, value=2)
        self.radio_button_dbscan.grid(row=1, column=2, padx=(20, 20), pady=(5, 10), sticky="n")

        self.main_button = customtkinter.CTkButton(self.main_frame, text="Load Dataset", border_width=2, width=410, command=self.main_button_event)
        self.main_button.grid(row=5, column=0, columnspan=3, padx=10, pady=(20, 20), sticky="w")

        #output_frame
        self.likes_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.likes_frame.grid(row=0, column=1, padx=(20, 20), pady=(20,0), sticky="nsew")
        self.label_likes = customtkinter.CTkLabel(self.likes_frame, text="Likes:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_likes.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="w")
        self.likes_textbox = customtkinter.CTkTextbox(self.likes_frame, width=175, height=300)
        self.likes_textbox.grid(row=1, column=0, padx=(10, 10), pady=(0, 0), sticky="nsew")

        self.dislikes_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.dislikes_frame.grid(row=0, column=2, padx=(20, 20), pady=(20,0), sticky="nsew")
        self.label_dislikes = customtkinter.CTkLabel(self.dislikes_frame, text="Dislikes:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_dislikes.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="w")
        self.dislikes_textbox = customtkinter.CTkTextbox(self.dislikes_frame, width=175, height=300)
        self.dislikes_textbox.grid(row=1, column=0, padx=(10, 10), pady=(0, 0), sticky="nsew")

    def main_button_event(self):
        path = self.entry_path.get()
        tweet = self.entry_tweet.get()
        sentiment = self.entry_sentiment.get()
        company = self.entry_company.get()
        clust_method = self.radio_var.get()

        df, pos_df, neg_df = implementation.preprocessing(path, tweet, sentiment, company)
        print(df.head())
        pos_vectors, neg_vectors, pos_feature_names, neg_feature_names= implementation.vectorization(pos_df, neg_df)

        if clust_method == 1:
            print("Hierarchical")
            pos_clusters, pos_df = implementation.hierarchical_clustering(pos_vectors, pos_feature_names, pos_df)
            neg_clusters, neg_df = implementation.hierarchical_clustering(neg_vectors, neg_feature_names, neg_df)
        elif clust_method == 2:
            print("Dbscan")
        else:
            pos_clusters, pos_df = implementation.k_means_clustering(pos_vectors, pos_feature_names, pos_df)
            neg_clusters, neg_df = implementation.k_means_clustering(neg_vectors, neg_feature_names, neg_df)

        pos_output_topics = implementation.topic_modelling(pos_clusters)
        neg_output_topics = implementation.topic_modelling(neg_clusters)

        pos_string = '\n'.join(['\n'.join(inner_topics) for inner_topics in pos_output_topics])
        neg_string = '\n'.join(['\n'.join(inner_topics) for inner_topics in neg_output_topics])

        self.likes_textbox.insert("0.0",pos_string)
        self.dislikes_textbox.insert("0.0",neg_string)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
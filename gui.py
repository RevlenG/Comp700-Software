
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
        self.geometry(f"{1100}x{500}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create the main input panel
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid(row=0, column=0, padx=(20, 10), pady=(20, 20), sticky="nsew")

        self.input_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=5, fg_color="transparent")
        self.input_frame.grid_columnconfigure((1, 2, 3), weight=1)
        self.input_frame.grid(row=0, column=0, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label_path = customtkinter.CTkLabel(self.input_frame, 
                                              text="Enter Dataset Path/Directory: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_path.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.entry_path = customtkinter.CTkEntry(self.input_frame, width=200)
        self.entry_path.grid(row=0, column=1, columnspan=3, padx=10, pady=(10, 0), sticky="nsew")

        self.label_tweet = customtkinter.CTkLabel(self.input_frame, 
                                              text="Enter Column Name for Reviews/Tweets: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_tweet.grid(row=1, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_tweet = customtkinter.CTkEntry(self.input_frame, width=200)
        self.entry_tweet.grid(row=1, column=1, columnspan=3, padx=10, pady=(20, 0), sticky="nsew")

        self.label_sentiment = customtkinter.CTkLabel(self.input_frame, 
                                              text="Enter Column Name for Sentiments: ", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_sentiment.grid(row=2, column=0, padx=10, pady=(15, 0), sticky="w")
        self.entry_sentiment = customtkinter.CTkEntry(self.input_frame, width=200)
        self.entry_sentiment.grid(row=2, column=1, columnspan=3, padx=10, pady=(20, 10), sticky="nsew")

        self.company_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=5, fg_color="transparent")
        self.company_frame.grid_columnconfigure((1, 2, 3), weight=1)
        self.company_frame.grid(row=1, column=0, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        self.label_companyq = customtkinter.CTkLabel(self.company_frame,
                                              text="Are all reviews in the dataset for the same company?", 
                                              font=customtkinter.CTkFont(size=13))
        self.label_companyq.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="w")

        self.radio_var = tkinter.IntVar(value=0)
        self.radio_button_yes = customtkinter.CTkRadioButton(self.company_frame, text="Yes", variable=self.radio_var, value=0, command=self.enable_disable_input)
        self.radio_button_yes.grid(row=0, column=1, padx=(20, 20), pady=(20, 10), sticky="n")
        self.radio_button_no = customtkinter.CTkRadioButton(self.company_frame, text="No", variable=self.radio_var, value=1, command=self.enable_disable_input)
        self.radio_button_no.grid(row=0, column=2, padx=(0, 20), pady=(20, 10), sticky="n")
        
        self.label_company = customtkinter.CTkLabel(self.company_frame,
                                              text="Enter Column Name for Companies: ", 
                                              font=customtkinter.CTkFont(size=13), text_color_disabled="#808080")
        self.label_company.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="w")
        self.entry_company = customtkinter.CTkEntry(self.company_frame, placeholder_text="")
        self.entry_company.grid(row=1, column=1, columnspan=3, padx=10, pady=(20, 0), sticky="nsew")

        self.label_company_name = customtkinter.CTkLabel(self.company_frame,
                                              text="Enter the Name of the Company for Review Clustering: ", 
                                              font=customtkinter.CTkFont(size=13), text_color_disabled="#808080")
        self.label_company_name.grid(row=2, column=0, padx=10, pady=(20, 0), sticky="w")
        self.entry_company_name = customtkinter.CTkEntry(self.company_frame, placeholder_text="")
        self.entry_company_name.grid(row=2, column=1, columnspan=3, padx=10, pady=(20, 0), sticky="nsew")


        self.radio_group_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=5)
        self.radio_group_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.radio_group_frame.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.radio_cluster_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(self.radio_group_frame, text="Clustering Method:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_radio_group.grid(row=0, column=1, padx=(20, 20), pady=(5, 5), sticky="nsew")
        self.radio_button_k_means = customtkinter.CTkRadioButton(self.radio_group_frame, text="K-Means Clustering", variable=self.radio_cluster_var, value=0)
        self.radio_button_k_means.grid(row=1, column=0, padx=(20, 20), pady=(5, 10), sticky="n")
        self.radio_button_hierarchical = customtkinter.CTkRadioButton(self.radio_group_frame, text="Heirarchical Clustering", variable=self.radio_cluster_var, value=1)
        self.radio_button_hierarchical.grid(row=1, column=1, padx=(20, 20), pady=(5, 10), sticky="n")
        self.radio_button_dbscan = customtkinter.CTkRadioButton(self.radio_group_frame, text="DBSCAN Clustering", variable=self.radio_cluster_var, value=2)
        self.radio_button_dbscan.grid(row=1, column=2, padx=(20, 20), pady=(5, 10), sticky="n")

        self.main_button = customtkinter.CTkButton(self.main_frame, text="Load Dataset and Perform Clustering", border_width=2, width=410, command=self.main_button_event)
        self.main_button.grid(row=5, column=0, columnspan=3, padx=10, pady=(20, 20), sticky="nsew")

        #output_frame
        self.likes_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.likes_frame.grid_columnconfigure(0, weight=1)
        self.likes_frame.grid_rowconfigure(1, weight=1)
        self.likes_frame.grid(row=0, column=1, padx=(10, 10), pady=(20,20), sticky="nsew")
        self.label_likes = customtkinter.CTkLabel(self.likes_frame, text="Likes:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_likes.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="w")
        self.likes_textbox = customtkinter.CTkTextbox(self.likes_frame, width=175, height=300)
        self.likes_textbox.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

        self.dislikes_frame = customtkinter.CTkFrame(self, corner_radius=5)
        self.dislikes_frame.grid_columnconfigure(0, weight=1)
        self.dislikes_frame.grid_rowconfigure(1, weight=1)
        self.dislikes_frame.grid(row=0, column=2, padx=(10, 20), pady=(20,20), sticky="nsew")
        self.label_dislikes = customtkinter.CTkLabel(self.dislikes_frame, text="Dislikes:", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label_dislikes.grid(row=0, column=0, padx=(20, 20), pady=(5, 5), sticky="w")
        self.dislikes_textbox = customtkinter.CTkTextbox(self.dislikes_frame, width=175, height=300)
        self.dislikes_textbox.grid(row=1, column=0, padx=(10, 10), pady=(0, 10), sticky="nsew")

        # set default values
        self.entry_company_name.configure(state="disabled")
        self.entry_company.configure(state="disabled")
        self.label_company_name.configure(state="disabled")
        self.label_company.configure(state="disabled")
        self.likes_textbox.configure(state="disabled")
        self.dislikes_textbox.configure(state="disabled")

    def main_button_event(self):
        path = self.entry_path.get()
        tweet = self.entry_tweet.get()
        sentiment = self.entry_sentiment.get()
        company = self.entry_company.get()
        clust_method = self.radio_cluster_var.get()

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


    def enable_disable_input(self):
        if self.radio_var.get() == 1:
            self.entry_company.configure(state="normal")
            self.entry_company_name.configure(state="normal")
            self.label_company.configure(state="normal")
            self.label_company_name.configure(state="normal")
        else:
            self.entry_company.delete(0, customtkinter.END)
            self.entry_company_name.delete(0, customtkinter.END)
            self.entry_company.configure(state="disabled")
            self.entry_company_name.configure(state="disabled")
            self.label_company.configure(state="disabled")
            self.label_company_name.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


if __name__ == "__main__":
    app = App()
    app.mainloop()
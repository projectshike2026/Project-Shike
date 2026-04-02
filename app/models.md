১. টেবিল ও কলাম তৈরি করার নিয়ম (The Basics)

যেকোনো টেবিল (যেমন User, Project, Note) তৈরি করার বেসিক নিয়ম একই। চলো User টেবিল দিয়ে বুঝি:

class User(UserMixin, db.Model):
    __tablename__ = 'users'


- class User(...): এটি ডেটাবেসের একটি টেবিলের ব্লুপ্রিন্ট। db.Model লেখার মানে হলো, ফ্লাস্ক একে একটি ডেটাবেস টেবিল হিসেবে ধরে নেবে। আর UserMixin ব্যবহার করা হয়েছে যাতে ফ্লাস্ক-লগইন (Flask-Login) বুঝতে পারে যে এটি ইউজারদের টেবিল এবং লগইন/লগআউট সহজে কাজ করে।

__tablename__ = 'users': পাইথনে ক্লাসের নাম দিয়েছ User, কিন্তু ডেটাবেসে এই টেবিলটির আসল নাম কী হবে, তা এখানে ঠিক করে দেওয়া হয়েছে।

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    profile_pic = db.Column(db.String(255), default='default.png')


db.Column(...): এর মানে তুমি টেবিলে একটি নতুন কলাম বা ফিল্ড যোগ করছ।

- db.Integer / db.String(50): এটা ডেটার ধরন (Data Type)। Integer মানে সংখ্যা (১,২,৩)। আর String(50) মানে এখানে টেক্সট বসবে, যার সর্বোচ্চ অক্ষর হবে ৫০টি। (তুমি চাইলে এডিট করে ৫০ এর জায়গায় ১০০ করে দিতে পারো!)

- primary_key=True: এটি এই টেবিলের আইডি বা রোল নাম্বার। দুজনের আইডি কখনো এক হবে পরিচয় হবে না।

- unique=True: এর মানে এই ডেটাটি সবার জন্য আলাদা হতে হবে। যেমন, দুজনের username বা email কখনো সেম হতে পারবে না। সেম হলে ডেটাবেস এরর দেবে।

- nullable=False: এর মানে এই ঘরটি ফাঁকা (Empty) রাখা যাবে না। ফর্ম পূরণের সময় এটা দিতেই হবে।

- default='default.png': যদি ইউজার কোনো ছবি না দেয়, তবে ডেটাবেস নিজ থেকেই এই ডিফল্ট নামটি বসিয়ে দেবে।



২. ক্লাসের ভেতরের ফাংশন (Methods)

User ক্লাসের ভেতর কিছু ফাংশন (def) লেখা আছে, যেগুলো খুব গুরুত্বপূর্ণ:

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


-  ইউজার যখন সাইন-আপ করার সময় পাসওয়ার্ড দেয় (যেমন: 12345), এই ফাংশনটি সেই পাসওয়ার্ড রিসিভ করে। এরপর generate_password_hash ব্যবহার করে সেটিকে একটি হিজিবিজি টেক্সটে (যেমন: pbkdf2:sha256:150000$xh7...) রূপান্তর করে password_hash কলামে সেভ করে।

কেন?: যাতে ডেটাবেস অ্যাডমিন বা হ্যাকার কেউ আসল পাসওয়ার্ড দেখতে না পারে।

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


কাজ: লগইন করার সময় ইউজার যে পাসওয়ার্ড দেয়, তার সাথে ডেটাবেসে সেভ করা হ্যাশ (hash) পাসওয়ার্ডটি মেলে কিনা, তা এই ফাংশনটি চেক করে। মিললে True রিটার্ন করে, না মিললে False।



৩. টেবিলের সাথে টেবিলের সম্পর্ক (Relationships)

এটি ডেটাবেস ডিজাইনের সবচেয়ে অ্যাডভান্সড এবং ইম্পরট্যান্ট পার্ট। একটি টেবিলের সাথে অন্য টেবিল কীভাবে যুক্ত থাকে, তা দেখো Project টেবিল থেকে:

    # Project টেবিলের ভেতরে:
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


- db.ForeignKey('users.id'): এটি একটি ব্রিজ বা সেতু। এটি বলে দিচ্ছে যে, "এই প্রজেক্টটি যে আপলোড করেছে, তার আইডি হলো users টেবিলের id"। এর ফলে আমরা জানতে পারি কোন প্রজেক্ট কার।

    # User টেবিলের ভেতরে:
    projects = db.relationship('Project', backref='author', lazy='dynamic')


- db.relationship(...): এটি ফ্লাস্কের ম্যাজিক! এটি ডেটাবেস কলাম নয়, বরং পাইথনের একটি লিংক।

- backref='author': এর মানে হলো, তুমি যদি প্রজেক্টের কোড থেকে ইউজারকে খুঁজতে চাও, তবে project.author লিখলেই ওই ইউজারের সব তথ্য চলে আসবে।

- lazy='dynamic': একজন ইউজারের হয়তো ৫০টি প্রজেক্ট আছে। dynamic দেওয়ার মানে হলো, পেজ লোড হওয়ার সাথে সাথেই ৫০টি প্রজেক্ট লোড করে অ্যাপ স্লো করবে না। যখন তুমি কোড করে চাইবে, ঠিক তখনই সে ডেটাবেস থেকে প্রজেক্টগুলো আনবে।

আরেকটি ইম্পরট্যান্ট রিলেশন ট্রিক (cascade):

    ratings = db.relationship('ProjectRating', backref='project', lazy='dynamic', cascade='all, delete-orphan')


cascade='all, delete-orphan': যদি কোনো ইউজার তার Project ডিলিট করে দেয়, তাহলে ডেটাবেসে ওই প্রজেক্টের ProjectRating (রেটিং/রিভিউ) গুলো অনাথ (orphan) হয়ে যাবে। cascade ব্যবহার করলে প্রজেক্ট ডিলিট হওয়ার সাথে সাথে তার সব রেটিং অটোমেটিক ডেটাবেস থেকে ডিলিট হয়ে যাবে। ফলে ডেটাবেসে আবর্জনা জমবে না।



৪. স্মার্ট ক্যালকুলেশন (@property)

- Project এবং MatchPerformance টেবিলে এই বিশেষ জিনিসটি আছে:

    @property
    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return round(self.total_rating / self.rating_count, 1)


@property কী?: এটি দেখতে ফাংশনের মতো, কিন্তু কাজ করে ভ্যারিয়েবলের মতো। এটি ডেটাবেসে কোনো জায়গা দখল করে না বা সেভ হয় না।

কাজ: যখনই  project.average_rating প্রিন্ট করবে, সে সাথে সাথে মোট রেটিংকে (total_rating) মোট মানুষ দিয়ে (rating_count) ভাগ করে গড় (Average) বের করবে। আর round(..., 1) মানে হলো দশমিকের পর ১ ঘর পর্যন্ত দেখাবে (যেমন: 4.5)।

পরিবর্তন করতে চাইলে: তুমি যদি চাও দশমিকের পর দুই ঘর দেখাক, তাহলে জাস্ট round(..., 2) করে দেবে!
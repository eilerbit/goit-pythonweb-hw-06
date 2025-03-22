import sys
import argparse
import shlex
from models import Session, Teacher, Group, Student

def create(session, model, name):
    cls = {"Teacher": Teacher, "Group": Group, "Student": Student}.get(model)
    if not cls:
        print("❌ Unsupported model for create")
        return
    obj = cls(name=name)
    session.add(obj)
    session.commit()
    print(f"✅ {model} '{name}' created successfully.")

def list_all(session, model):
    cls = {"Teacher": Teacher, "Group": Group, "Student": Student}.get(model)
    if not cls:
        print("❌ Unsupported model for list")
        return
    objs = session.query(cls).all()
    for obj in objs:
        print(f"{obj.id}: {obj.name}")

def update(session, model, obj_id, new_name):
    cls = {"Teacher": Teacher, "Group": Group, "Student": Student}.get(model)
    if not cls:
        print("❌ Unsupported model for update")
        return
    obj = session.query(cls).filter_by(id=obj_id).first()
    if obj:
        obj.name = new_name
        session.commit()
        print(f"✅ {model} with ID {obj_id} updated to '{new_name}'.")
    else:
        print(f"❌ {model} not found.")

def remove(session, model, obj_id):
    cls = {"Teacher": Teacher, "Group": Group, "Student": Student}.get(model)
    if not cls:
        print("❌ Unsupported model for remove")
        return
    obj = session.query(cls).filter_by(id=obj_id).first()
    if obj:
        session.delete(obj)
        session.commit()
        print(f"✅ {model} with ID {obj_id} deleted.")
    else:
        print(f"❌ {model} not found.")

def get_arguments():
    parser = argparse.ArgumentParser(description="Manage database records.")
    parser.add_argument("-a", "--action", required=True, help="Action to perform (create, list, update, remove)")
    parser.add_argument("-m", "--model", required=True, choices=["Teacher", "Group", "Student"], help="Model to act upon")
    parser.add_argument("--id", type=int, help="ID of the record to update or delete")
    parser.add_argument("-n", "--name", help="Name for create or update")
    return parser.parse_args()


def main():
    while True:
        if len(sys.argv) == 1:
            user_input = input("Enter your arguments (or type 'exit' to quit) or use --help: ").strip()
            if user_input.lower() == "exit":
                print("👋 Exiting...")
                break
            sys.argv.extend(shlex.split(user_input))

        args = get_arguments()

        valid_actions = ["create", "list", "update", "remove"]
        if args.action not in valid_actions:
            print(f"❌ Invalid action '{args.action}'. Allowed: create, list, update, remove")
            sys.argv = [sys.argv[0]]  # Reset argv
            continue

        session = Session()
        try:
            if args.action == "create" and args.name:
                create(session, args.model, args.name)
            elif args.action == "list":
                list_all(session, args.model)
            elif args.action == "update" and args.id and args.name:
                update(session, args.model, args.id, args.name)
            elif args.action == "remove" and args.id:
                remove(session, args.model, obj_id=args.id)
            else:
                print("❌ Invalid command. Use --help for usage instructions.")
        finally:
            session.close()

        # Reset sys.argv
        sys.argv = [sys.argv[0]]

if __name__ == "__main__":
    main()

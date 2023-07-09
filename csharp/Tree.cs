using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Demo
{
    /// <summary>
    /// 树节点。
    /// </summary>
    public class TreeNode<T>
    {
        /// <summary>
        /// 数据。
        /// </summary>
        public List<T>? Data = null;

        /// <summary>
        /// 子节点。
        /// </summary>
        public virtual List<TreeNode<T>>? Children { get; }

        /// <summary>
        /// 前序遍历。
        /// </summary>
        /// <returns></returns>
        public virtual List<T> PreorderTraversal()
        {
            var all = new List<T>();
            if (Data != null)
            {
                all.AddRange(Data);
            }
            if (Children != null)
            {
                foreach (var child in Children)
                {
                    all.AddRange(child.PreorderTraversal());
                }
            }
            return all;
        }

        /// <summary>
        /// 后续遍历。
        /// </summary>
        /// <returns></returns>
        public virtual List<T> PostorderTraversal()
        {
            var all = new List<T>();
            if (Data != null)
            {
                all.AddRange(Data);
            }
            if (Children != null)
            {
                foreach (var child in Children)
                {
                    all.AddRange(child.PostorderTraversal());
                }
            }
            return all;
        }
    }

    /// <summary>
    /// 树。
    /// </summary>
    /// <typeparam name="T"></typeparam>
    public class Tree<T>
    {
        /// <summary>
        /// 根节点。
        /// </summary>
        public TreeNode<T>? Root;

        /// <summary>
        /// 前序遍历。
        /// </summary>
        /// <returns></returns>
        public virtual List<T> PreorderTraversal()
        {
            return Root == null ? new List<T>() : Root.PreorderTraversal();
        }

        /// <summary>
        /// 后序遍历。
        /// </summary>
        /// <returns></returns>
        public virtual List<T> PostorderTraversal()
        {
            return Root == null ? new List<T>() : Root.PostorderTraversal();
        }
    }
}
